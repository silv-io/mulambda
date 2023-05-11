import abc
from collections import UserDict
from typing import Any, Dict, Literal, Tuple

from mulambda.util import Number

ModelType = Literal[
    "classification", "regression", "debug", "completion", "translation"
]
DataType = Literal["image", "text", "audio", "video", "tabular"]


class MatchedTrait(abc.ABC):
    def __init__(self, trait):
        self.trait = trait

    @abc.abstractmethod
    def match(self, other) -> bool:
        raise NotImplementedError


class EqualityTrait(MatchedTrait):
    def match(self, other) -> bool:
        return self.trait == other


class MinTrait(MatchedTrait):
    def match(self, other) -> bool:
        return self.trait <= other


class MaxTrait(MatchedTrait):
    def match(self, other) -> bool:
        return self.trait >= other


class RequiredTraits(UserDict):
    def __init__(
        self,
        model_type: EqualityTrait,
        input_type: EqualityTrait,
        output_format: EqualityTrait,
        **kwargs,
    ):
        super().__init__()
        self.data: Dict[str, MatchedTrait] = {
            "type": model_type,
            "input": input_type,
            "output": output_format,
        } | kwargs


class DesiredTraitWeights(UserDict):
    # use negative weights for traits that should be maximized
    def __init__(
        self,
        latency: int,
        accuracy: int,
        **kwargs,
    ):
        super().__init__()
        self.data: Dict[str, Any] = {
            "latency": latency,
            "accuracy": accuracy,
        } | kwargs


class NormalizationRanges(UserDict):
    def __init__(self, latency: Tuple[int, int], **kwargs):
        super().__init__()
        self.data: Dict[str, Tuple[Number, Number]] = {"latency": latency} | kwargs


class ModelTraits(UserDict):
    def __init__(
        self,
        identity: str,
        model_type: ModelType,
        input_type: DataType,
        output_type: DataType,
        latency: int,
        accuracy: float,
        **kwargs,
    ):
        super().__init__()
        self.data: Dict[str, Any] = {
            "id": identity,
            "type": model_type,
            "input": input_type,
            "output": output_type,
            "latency": latency,
            "accuracy": accuracy,
        } | kwargs

    def hard_filter(self, required_traits: RequiredTraits) -> bool:
        return all(
            trait.match(self.data[key]) for key, trait in required_traits.items()
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
            k: _normalize(k, v) * weights.get(k, 0)
            for k, v in self.data.items()
            if v is not None and type(v) is Number
        }
        return 1 - sum(normalized.values())
