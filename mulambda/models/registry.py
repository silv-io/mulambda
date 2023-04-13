from typing import Dict

from mulambda.models.inference import ModelInferencer
from mulambda.models.matching import ModelCharacteristics, SoftCriteriaWeights, HardCriteria

dummy_model_characteristics = ModelCharacteristics(
    hard_criteria={'model_type': 'dummy', 'input_type': 'text', 'output_format': 'text'},
    soft_criteria={'energy_efficiency': 1.0, 'accuracy': 1.0, 'latency': 10, 'cached': False},
    version=1
)


class IdentityInferencer(ModelInferencer):
    def __init__(self, identity: str):
        self.identity = identity
        super().__init__()

    def infer(self, input_data):
        return f"[{self.identity}] received: {input_data}"


class Model:
    characteristics: ModelCharacteristics
    inferencer: ModelInferencer

    def __init__(self, characteristics: ModelCharacteristics = None, inferencer: ModelInferencer = None):
        self.characteristics = characteristics or dummy_model_characteristics
        self.inferencer = inferencer or IdentityInferencer(self.characteristics.identity)


class ModelRegistry:
    models: Dict[str, Model]

    def __init__(self):
        self.models = {}

    def register_model(self, model: Model):
        self.models[model.characteristics.identity] = model

    def receive_model(self, hard_criteria: HardCriteria, weights: SoftCriteriaWeights):
        return min(self.models.values(),
                   key=lambda model: ModelCharacteristics.generate_key_function(hard_criteria, weights)(
                       model.characteristics))


MODELS = ModelRegistry()
