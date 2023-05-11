import asyncio
import logging
from typing import List, Tuple

import ray
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from starlette.requests import Request

from mulambda.infra.base_model import ModelInput
from mulambda.infra.traits import (
    DesiredTraitWeights,
    EqualityTrait,
    ModelTraits,
    NormalizationRanges,
    RequiredTraits,
)

LOG = logging.getLogger(__name__)


@serve.deployment
class ModelSelector:
    models: List[Tuple[ModelTraits, RayServeDeploymentHandle]]

    def __init__(self, models: List[Tuple[ModelTraits, RayServeDeploymentHandle]]):
        self.models = models

    async def _select(
        self,
        required: RequiredTraits,
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
    ) -> RayServeDeploymentHandle:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        return min(filtered, key=lambda model: model[0].sort_key(weights, ranges))[1]

    async def __call__(self, http_request: Request):
        request = await http_request.json()
        required = RequiredTraits(
            EqualityTrait(request["required"]["type"]),
            EqualityTrait(request["required"]["input"]),
            EqualityTrait(request["required"]["output"]),
        )
        weights = DesiredTraitWeights(
            request["desired"]["latency"], request["desired"]["accuracy"]
        )
        ranges = NormalizationRanges(request["ranges"]["latency"])

        selected: RayServeDeploymentHandle = await self._select(
            required, weights, ranges
        )

        submission_task: asyncio.Task = selected.remote(
            ModelInput(input=request["input"])
        )
        ref: ray.ObjectRef = await submission_task
        LOG.debug(f"Request {http_request} assigned to replica {ref}")
        result = await ref
        LOG.debug(
            f"Request {http_request} processed by replica {ref} with result {result}"
        )

        return result
