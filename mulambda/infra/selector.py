import logging
import random
from typing import Any, Dict, List, Tuple

from redis.asyncio.client import Redis

from mulambda.config import settings
from mulambda.infra.traits import (
    ModelTraits,
    RequiredTraits,
    estimate_performance,
)
from mulambda.util import MULAMBDA_MODELS, get_metadata_server

LOG = logging.getLogger(__name__)

Endpoint = str


def get_score(weights: Dict[str, float], latency, accuracy) -> float:
    return -weights["latency"] * latency + weights["accuracy"] * accuracy


def normalize_latency(latency: int) -> float:
    buckets = settings.selector.latency_buckets
    for i, bucket in enumerate(buckets):
        if latency <= bucket:
            return round(1 - (i / len(buckets)), 2)
    else:
        return 0.0


class ModelSelector:
    models: List[Tuple[ModelTraits, Endpoint]]

    def __init__(self):
        self.models = []

    def append(self, model: Tuple[ModelTraits, Endpoint]):
        self.models.append(model)

    def _select(
        self,
        required: RequiredTraits,
        weights: Dict[str, float],
        data_length: int,
        client_id: str,
    ) -> Tuple[ModelTraits, Endpoint]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        estimate = [
            (estimate_performance(model[0], data_length, client_id), model[1])
            for model in filtered
        ]
        max_accuracy = max(estimate, key=lambda x: x[0][2])[0][2]
        normalized = [
            (
                model[0][0],
                normalize_latency(model[0][1]),
                model[0][2] / max_accuracy,
                model[1],
            )
            for model in estimate
        ]
        selected = max(normalized, key=lambda x: get_score(weights, x[1], x[2]))
        return selected[0], selected[3]

    def __call__(
        self,
        client_id: str,
        request: Dict[str, Any],
    ) -> Dict[str, Any]:
        required = RequiredTraits(
            request["required"]["type"],
            request["required"]["input"],
            request["required"]["output"],
        )

        traits, selected = self._select(
            required, request["desired"], request["data_length"], client_id
        )

        print(f"Selected model: {traits}")

        return {
            "endpoint": selected,
            "model": traits.data,
        }

    async def ingest_models(self, r: Redis):
        model_ids = await r.smembers(MULAMBDA_MODELS)
        for model_id in model_ids:
            traits = ModelTraits.from_redis(
                await r.hgetall(f"{MULAMBDA_MODELS}:{model_id}")
            )
            endpoint = f"{model_id}.{settings.network.base}"
            self.models.append((traits, endpoint))


class RoundRobinSelector(ModelSelector):
    index: int

    def __init__(self):
        super().__init__()
        self.index = 0

    def _select(
        self,
        required: RequiredTraits,
        weights: Dict[str, float],
        data_length: int,
        client_id: str,
    ) -> Tuple[ModelTraits, Endpoint]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        selected = filtered[self.index % len(filtered)]
        self.index += 1
        return selected


class RandomSelector(ModelSelector):
    def _select(
        self,
        required: RequiredTraits,
        weights: Dict[str, float],
        data_length: int,
        client_id: str,
    ) -> Tuple[ModelTraits, Endpoint]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        return random.choice(filtered)


class PlainNetLatencySelector(ModelSelector):
    def _select(
        self,
        required: RequiredTraits,
        weights: Dict[str, float],
        data_length: int,
        client_id: str,
    ) -> Tuple[ModelTraits, Endpoint]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        return min(filtered, key=lambda x: x[0]["latencies"][client_id])


if settings.selector.type == "round-robin":
    selector = RoundRobinSelector()
else:
    selector = ModelSelector()


async def get_selector() -> ModelSelector:
    redis = get_metadata_server()
    await selector.ingest_models(redis)
    return selector
