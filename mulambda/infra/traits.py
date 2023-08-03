import abc
from collections import UserDict
from typing import Any, Dict


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


class ModelTraits(UserDict):
    def __init__(
        self,
        identity: str,
        model_type: str,
        input_type: str,
        output_type: str,
        mdd: float,
        latencies: Dict[str, int],
        accuracy: float,
        path: str,
        port: int,
        **kwargs,
    ):
        super().__init__()
        self.data: Dict[str, Any] = {
            "id": identity,
            "type": model_type,
            "input": input_type,
            "output": output_type,
            "mdd": mdd,  # model data delay
            "latencies": latencies,
            "accuracy": accuracy,
            "path": path,
            "port": port,
        } | kwargs

    @staticmethod
    def from_redis(data: Dict[str, str]) -> "ModelTraits":
        return ModelTraits(
            identity=data["id"],
            model_type=data["type"],
            input_type=data["input"],
            output_type=data["output"],
            mdd=float(data.get("mdd", 0)),
            latencies={
                k.removeprefix("latency:"): v
                for k, v in data.items()
                if k.startswith("latency:")
            },
            accuracy=float(data["accuracy"]),
            path=data["path"],
            port=int(data["port"]),
        )

    def hard_filter(self, required_traits: RequiredTraits) -> bool:
        return all(
            trait.match(self.data[key]) for key, trait in required_traits.items()
        )

    def estimate_latency(self, data_length: int, client_id: str) -> float:
        return self.data["latencies"][client_id] + self.data["mdd"] * data_length


def estimate_performance(
    traits: ModelTraits, data_length: int, client_id: str
) -> (ModelTraits, float, float):
    latency_estimate = traits.estimate_latency(data_length, client_id)
    accuracy = traits["accuracy"]
    return traits, latency_estimate, accuracy
