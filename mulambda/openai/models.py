from mulambda.models.matching import ModelCharacteristics
from mulambda.models.registry import Model
from mulambda.openai.executor import GPTExecutor

_gpt_hard_criteria = {
    "model_type": "prompt",
    "input_type": "text",
    "output_format": "text",
}
_ada = Model(
    characteristics=ModelCharacteristics(
        hard_criteria=_gpt_hard_criteria,
        version=1,
        identity="ada",
        soft_criteria={  # some dummy values
            "latency": 100,
            "energy_efficiency": 0.5,
            "accuracy": 0.9,
            "cached": False,
        },
    ),
    executor=GPTExecutor(model_id="text-ada-001"),
)

MODELS = [_ada]
