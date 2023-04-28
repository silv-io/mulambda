import asyncio
import logging
from typing import List

import ray
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from starlette.requests import Request

from mulambda.infra.traits import (
    DesiredTraitWeights,
    EqualityTrait,
    NormalizationRanges,
    RequiredTraits,
)

LOG = logging.getLogger(__name__)


@serve.deployment
class ModelSelector:
    models: List[RayServeDeploymentHandle]

    def __init__(self, models: List[RayServeDeploymentHandle]):
        self.models = models

    def _select(
        self,
        required: RequiredTraits,
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
    ) -> RayServeDeploymentHandle:
        filtered = [model for model in self.models if model.hard_filter(required)]
        return min(filtered, key=lambda model: model.sort_key(weights, ranges))

    async def __call__(self, http_request: Request):
        # TODO handle input
        required = RequiredTraits(
            EqualityTrait("prompt"), EqualityTrait("text"), EqualityTrait("text")
        )
        weights = DesiredTraitWeights(latency=-1, accuracy=1)
        # TODO handle normalization range detection
        ranges = NormalizationRanges(latency=(0, 500))

        selected: RayServeDeploymentHandle = self._select(required, weights, ranges)
        request = await http_request.json()

        submission_task: asyncio.Task = selected.remote(request)
        ref: ray.ObjectRef = await submission_task
        LOG.debug(f"Request {http_request} assigned to replica {ref}")
        result = await ref
        LOG.debug(
            f"Request {http_request} processed by replica {ref} with result {result}"
        )

        return result
