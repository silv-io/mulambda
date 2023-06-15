import logging
from typing import Any, Dict, List, Tuple

from mulambda.infra.base_model import BaseModelBackend, ModelInput
from mulambda.infra.traits import (
    DesiredTraitWeights,
    ModelTraits,
    NormalizationRanges,
    RequiredTraits,
)

LOG = logging.getLogger(__name__)


class ModelSelector:
    models: List[Tuple[ModelTraits, BaseModelBackend]]

    def __init__(self, models: List[Tuple[ModelTraits, BaseModelBackend]]):
        self.models = models

    def append(self, model: Tuple[ModelTraits, BaseModelBackend]):
        self.models.append(model)

    def _select(
        self,
        required: RequiredTraits,
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
    ) -> Tuple[ModelTraits, BaseModelBackend]:
        filtered = [model for model in self.models if model[0].hard_filter(required)]
        return min(filtered, key=lambda model: model[0].sort_key(weights, ranges))

    async def __call__(self, request: Dict[str, Any]) -> str:
        required = RequiredTraits(
            request["required"]["type"],
            request["required"]["input"],
            request["required"]["output"],
        )
        weights = DesiredTraitWeights(
            request["desired"]["latency"], request["desired"]["accuracy"]
        )
        ranges = NormalizationRanges(request["ranges"]["latency"])

        traits, selected = self._select(required, weights, ranges)

        result = await selected(ModelInput(input=request["input"]))

        return f"model {traits['id']} returned {result}"
