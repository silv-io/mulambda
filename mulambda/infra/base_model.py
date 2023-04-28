import abc
from typing import Any, TypedDict

from mulambda.infra.selector import (
    DesiredTraitWeights,
    NormalizationRanges,
    RequiredTraits,
)
from mulambda.infra.traits import ModelTraits

ModelInput = TypedDict("ModelInput", {"input": Any})


class BaseModel(abc.ABC):
    traits: ModelTraits

    def __init__(self, traits: ModelTraits):
        super().__init__()
        self.traits = traits

    def hard_filter(self, required_traits: RequiredTraits) -> bool:
        return all(
            trait.match(self.traits[key]) for key, trait in required_traits.items()
        )

    def sort_key(
        self,
        weights: DesiredTraitWeights,
        ranges: NormalizationRanges,
    ) -> float:
        def _normalize(key, value):
            if key not in ranges:
                return value
            min_, max_ = ranges[key]
            return (value - min_) / (max_ - min_)

        normalized = {
            k: _normalize(k, v) * weights[k]
            for k, v in self.traits.items()
            if v is not None
        }
        return 1 - sum(normalized.values())

    @abc.abstractmethod
    def __call__(self, request: ModelInput) -> Any:
        pass
