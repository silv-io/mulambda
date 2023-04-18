from typing import Dict

from mulambda.models.executor import IdentityExecutor, ModelExecutor
from mulambda.models.matching import (
    HardCriteria,
    ModelCharacteristics,
    SoftCriteriaWeights,
)

dummy_model_characteristics = ModelCharacteristics(
    hard_criteria={
        "model_type": "dummy",
        "input_type": "text",
        "output_format": "text",
    },
    soft_criteria={
        "energy_efficiency": 1.0,
        "accuracy": 1.0,
        "latency": 10,
        "cached": False,
    },
    version=1,
)


class Model:
    characteristics: ModelCharacteristics
    executor: ModelExecutor

    def __init__(
        self,
        characteristics: ModelCharacteristics = None,
        executor: ModelExecutor = None,
    ):
        self.characteristics = characteristics or dummy_model_characteristics
        self.executor = executor or IdentityExecutor()


class ModelRegistry:
    models: Dict[str, Model]

    def __init__(self):
        self.models = {}

    def register_model(self, model: Model):
        self.models[model.characteristics.identity] = model

    def receive_model(self, hard_criteria: HardCriteria, weights: SoftCriteriaWeights):
        return min(
            self.models.values(),
            key=lambda model: ModelCharacteristics.generate_key_function(
                hard_criteria, weights
            )(model.characteristics),
        )
