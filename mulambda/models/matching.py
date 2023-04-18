from typing import Callable, Literal, TypedDict

from mulambda.util import short_uid


class HardCriteria(TypedDict):
    model_type: Literal["classification", "regression", "dummy"]
    input_type: Literal["image", "text", "audio", "video", "tabular"]
    output_format: Literal["image", "text", "audio", "video", "tabular"]


class SoftCriteria(TypedDict):
    energy_efficiency: float  # in [0, 1]
    accuracy: float  # in [0, 1]
    latency: int  # in ms
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


class ModelCharacteristics:
    hard_criteria: HardCriteria
    soft_criteria: SoftCriteria
    identity: str
    version: int

    def __init__(
        self,
        hard_criteria: HardCriteria,
        soft_criteria: SoftCriteria,
        version: int = 0,
        identity: str = None,
    ):
        self.hard_criteria = hard_criteria
        self.soft_criteria = soft_criteria
        self.version = version
        self.identity = identity or short_uid()

    @classmethod
    def _normalize_latency(cls, latency: int, latency_range: LatencyRange) -> float:
        return (latency - latency_range["min"]) / (
            latency_range["max"] - latency_range["min"]
        )

    @classmethod
    def _get_weighted_score(cls, model, hard_criteria, weights):
        if model.hard_criteria != hard_criteria:
            return float("inf")
        return (
            1
            - model.soft_criteria["accuracy"] * weights["accuracy"]
            + cls._normalize_latency(
                model.soft_criteria["latency"], weights["latency_range"]
            )
            * weights["latency"]
            + model.soft_criteria["energy_efficiency"] * weights["energy_efficiency"]
            + (1 - int(model.soft_criteria["cached"])) * weights["cached"]
        )

    @classmethod
    def generate_key_function(
        cls, hard_criteria: HardCriteria, weights: SoftCriteriaWeights
    ) -> Callable:
        def key_function(model: ModelCharacteristics):
            return cls._get_weighted_score(model, hard_criteria, weights)

        return key_function

    def __repr__(self):
        return f"ModelCharacteristics({self.hard_criteria}, {self.soft_criteria}, {self.version})"


if __name__ == "__main__":
    models = [
        ModelCharacteristics(
            hard_criteria={
                "model_type": "classification",
                "input_type": "image",
                "output_format": "text",
            },
            soft_criteria={
                "energy_efficiency": 0.8,
                "accuracy": 0.9,
                "latency": 50,
                "cached": True,
            },
            version=1,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "regression",
                "input_type": "tabular",
                "output_format": "audio",
            },
            soft_criteria={
                "energy_efficiency": 0.5,
                "accuracy": 0.7,
                "latency": 100,
                "cached": False,
            },
            version=2,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "classification",
                "input_type": "text",
                "output_format": "image",
            },
            soft_criteria={
                "energy_efficiency": 0.6,
                "accuracy": 0.8,
                "latency": 70,
                "cached": True,
            },
            version=3,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "regression",
                "input_type": "audio",
                "output_format": "tabular",
            },
            soft_criteria={
                "energy_efficiency": 0.7,
                "accuracy": 0.85,
                "latency": 80,
                "cached": False,
            },
            version=4,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "classification",
                "input_type": "image",
                "output_format": "audio",
            },
            soft_criteria={
                "energy_efficiency": 0.9,
                "accuracy": 0.95,
                "latency": 30,
                "cached": True,
            },
            version=5,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "regression",
                "input_type": "tabular",
                "output_format": "text",
            },
            soft_criteria={
                "energy_efficiency": 0.8,
                "accuracy": 0.6,
                "latency": 90,
                "cached": False,
            },
            version=6,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "classification",
                "input_type": "audio",
                "output_format": "tabular",
            },
            soft_criteria={
                "energy_efficiency": 0.7,
                "accuracy": 0.75,
                "latency": 60,
                "cached": True,
            },
            version=7,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "regression",
                "input_type": "text",
                "output_format": "image",
            },
            soft_criteria={
                "energy_efficiency": 0.6,
                "accuracy": 0.85,
                "latency": 40,
                "cached": False,
            },
            version=8,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "classification",
                "input_type": "image",
                "output_format": "tabular",
            },
            soft_criteria={
                "energy_efficiency": 0.9,
                "accuracy": 0.99,
                "latency": 20,
                "cached": True,
            },
            version=9,
        ),
        ModelCharacteristics(
            hard_criteria={
                "model_type": "regression",
                "input_type": "tabular",
                "output_format": "audio",
            },
            soft_criteria={
                "energy_efficiency": 0.5,
                "accuracy": 0.8,
                "latency": 120,
                "cached": False,
            },
            version=10,
        ),
    ]

    sorted = sorted(
        models,
        key=ModelCharacteristics.generate_key_function(
            hard_criteria={
                "model_type": "regression",
                "input_type": "tabular",
                "output_format": "audio",
            },
            weights={
                "energy_efficiency": 1,
                "accuracy": 1,
                "latency": 1,
                "latency_range": {"min": 20, "max": 120},
                "cached": 1,
            },
        ),
    )

    print(sorted)
