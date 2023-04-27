import asyncio
import logging
from typing import Dict, Literal, TypedDict

import ray
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from starlette.requests import Request

LOG = logging.getLogger(__name__)


class HardCriteria(TypedDict):
    model_type: Literal["classification", "regression", "dummy", "prompt"]
    input_type: Literal["image", "text", "audio", "video", "tabular"]
    output_format: Literal["image", "text", "audio", "video", "tabular"]


# TODO add a cost vector
class SoftCriteria(TypedDict):
    energy_efficiency: float  # in [0, 1]
    accuracy: float  # in [0, 1]
    latency: int  # in ms # todo add historic latency
    cached: bool  # True if the model is cached


class LatencyRange(TypedDict):
    min: int
    max: int


class SoftCriteriaWeights(TypedDict):
    energy_efficiency: int
    accuracy: int
    latency: int
    latency_range: LatencyRange
    cached: int


@serve.deployment
class ModelSelector:
    models: Dict[str, RayServeDeploymentHandle]

    def __init__(self, models: Dict[str, RayServeDeploymentHandle]):
        self.models = models

    def _select(self, hard_criteria: HardCriteria, soft_criteria: SoftCriteriaWeights):
        # TODO return the best model, rethink maybe how to organize criteria
        pass

    async def __call__(self, http_request: Request):
        # TODO handle input
        selected = list(self.models.values())[0]
        request = await http_request.json()

        submission_task: asyncio.Task = selected.remote(request)
        ref: ray.ObjectRef = await submission_task
        LOG.debug(f"Request {http_request} assigned to replica {ref}")
        result = await ref
        LOG.debug(
            f"Request {http_request} processed by replica {ref} with result {result}"
        )

        return result
