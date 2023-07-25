import logging
import random
from typing import Any, Dict, List, Tuple

from redis.asyncio.client import Redis

from mulambda.config import settings
from mulambda.infra.traits import (
    DesiredTraitWeights,
    ModelTraits,
    NormalizationRanges,
    RequiredTraits,
)
from mulambda.util import MULAMBDA_MODELS, get_metadata_server

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
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
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
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
        client_id: str,
    ) -> Tuple[ModelTraits, Endpoint]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        return random.choice(filtered)


if settings.selector.type == "round-robin":
    selector = RoundRobinSelector()
else:
    selector = ModelSelector()


async def get_selector() -> ModelSelector:
    redis = get_metadata_server()
    await selector.ingest_models(redis)
    return selector
