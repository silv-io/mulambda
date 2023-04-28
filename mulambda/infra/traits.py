import abc
from collections import UserDict
from typing import Any, Dict, Generic, Literal, Tuple, TypeVar

from mulambda.util import Number

ModelType = Literal["classification", "regression", "debug", "completion"]
DataType = Literal["image", "text", "audio", "video", "tabular"]


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


TraitType = TypeVar("TraitType")


class MatchedTrait(Generic[TraitType], abc.ABC):
    def __init__(self, trait: TraitType):
        self.trait = trait

    @abc.abstractmethod
    def match(self, other: TraitType) -> bool:
        raise NotImplementedError


class EqualityTrait(MatchedTrait):
    def match(self, other: TraitType) -> bool:
        return self.trait == other


class MinTrait(MatchedTrait):
    def match(self, other: TraitType) -> bool:
        return self.trait <= other


class MaxTrait(MatchedTrait):
    def match(self, other: TraitType) -> bool:
        return self.trait >= other


class RequiredTraits(UserDict):
    def __init__(
        self,
        model_type: EqualityTrait[
            Literal["classification", "regression", "dummy", "prompt"]
        ],
        input_type: EqualityTrait[
            Literal["image", "text", "audio", "video", "tabular"]
        ],
        output_format: EqualityTrait[
            Literal["image", "text", "audio", "video", "tabular"]
        ],
        **kwargs,
    ):
        super().__init__()
        self.data: Dict[str, MatchedTrait] = {
            "model_type": model_type,
            "input_type": input_type,
            "output_format": output_format,
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
