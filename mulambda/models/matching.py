from typing import Callable

from ray import serve

from mulambda.infra.selector import (
    HardCriteria,
    LatencyRange,
    SoftCriteria,
    SoftCriteriaWeights,
)
from mulambda.models.registry import ModelRegistry
from mulambda.util import short_uid


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
        return (
            f"ModelCharacteristics({self.hard_criteria}, {self.soft_criteria},"
            f"{self.version})"
        )


@serve.deployment
class ModelMatcher:
    registry: ModelRegistry

    def __init__(self, registry: ModelRegistry):
        self.registry = registry
