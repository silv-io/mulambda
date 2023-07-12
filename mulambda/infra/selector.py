import logging
from typing import Any, Dict, List, Tuple

from redis import asyncio as aioredis

from mulambda.config import settings
from mulambda.infra.traits import (
    DesiredTraitWeights,
    ModelTraits,
    NormalizationRanges,
    RequiredTraits,
)
from mulambda.util import REDIS_MODELS

LOG = logging.getLogger(__name__)

Endpoint = str


class ModelSelector:
    models: List[Tuple[ModelTraits, Endpoint]]

    def __init__(self):
        self.models = []

    def append(self, model: Tuple[ModelTraits, Endpoint]):
        self.models.append(model)

    def _select(
        self,
        required: RequiredTraits,
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
        client_id: str,
    ) -> Tuple[ModelTraits, Endpoint]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        return min(
            filtered, key=lambda model: model[0].sort_key(weights, ranges, client_id)
        )

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
        weights = DesiredTraitWeights(
            request["desired"]["latency"], request["desired"]["accuracy"]
        )
        ranges = NormalizationRanges(request["ranges"]["latency"])

        traits, selected = self._select(required, weights, ranges, client_id)

        print(f"Selected model: {traits}")

        return {
            "endpoint": selected,
            "model": traits.data,
        }

    async def ingest_models(self, r: aioredis.Redis):
        model_ids = await r.smembers(REDIS_MODELS)
        for model_id in model_ids:
            traits = ModelTraits.from_redis(
                await r.hgetall(f"{REDIS_MODELS}:{model_id}")
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
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
        client_id: str,
    ) -> Tuple[ModelTraits, Endpoint]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        selected = filtered[self.index % len(filtered)]
        self.index += 1
        return selected


if settings.selector.type == "round-robin":
    selector = RoundRobinSelector()
else:
    selector = ModelSelector()


async def get_selector() -> ModelSelector:
    redis = await aioredis.from_url(
        f"redis://{settings.network.redis}.{settings.network.base}",
        # "redis://localhost:6379",
        encoding="utf-8",
        decode_responses=True,
    )
    await selector.ingest_models(redis)
    return selector
