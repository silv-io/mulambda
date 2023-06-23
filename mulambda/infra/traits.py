import abc
from collections import UserDict
from typing import Any, Dict, Tuple

from mulambda.util import Number


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
        model_type: str,
        input_type: str,
        output_format: str,
        **kwargs,
    ):
        super().__init__()
        self.data: Dict[str, MatchedTrait] = {
            "type": EqualityTrait(model_type),
            "input": EqualityTrait(input_type),
            "output": EqualityTrait(output_format),
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
        model_type: str,
        input_type: str,
        output_type: str,
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

    @staticmethod
    def from_redis(data: Dict[str, str]) -> "ModelTraits":
        print(data)
        return ModelTraits(
            identity=data["id"],
            model_type=data["type"],
            input_type=data["input"],
            output_type=data["output"],
            latency=int(data["latency"]),
            accuracy=float(data["accuracy"]),
        )

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
            if v is not None and (type(v) is int or type(v) is float)
        }
        return 1 - sum(normalized.values())
