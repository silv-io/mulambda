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
_babbage = Model(
    characteristics=ModelCharacteristics(
        hard_criteria=_gpt_hard_criteria,
        version=1,
        identity="babbage",
        soft_criteria={  # some dummy values
            "latency": 110,
            "energy_efficiency": 0.5,
            "accuracy": 0.95,
            "cached": False,
        },
    ),
    executor=GPTExecutor(model_id="text-babbage-001"),
)
_curie = Model(
    characteristics=ModelCharacteristics(
        hard_criteria=_gpt_hard_criteria,
        version=1,
        identity="curie",
        soft_criteria={  # some dummy values
            "latency": 120,
            "energy_efficiency": 0.5,
            "accuracy": 0.975,
            "cached": False,
        },
    ),
    executor=GPTExecutor(model_id="text-curie-001"),
)
_davinci_1 = Model(
    characteristics=ModelCharacteristics(
        hard_criteria=_gpt_hard_criteria,
        version=1,
        identity="davinci",
        soft_criteria={  # some dummy values
            "latency": 140,
            "energy_efficiency": 0.5,
            "accuracy": 0.975,
            "cached": False,
        },
    ),
    executor=GPTExecutor(model_id="text-davinci-001"),
)
_davinci_2 = Model(
    characteristics=ModelCharacteristics(
        hard_criteria=_gpt_hard_criteria,
        version=2,
        identity="davinci",
        soft_criteria={  # some dummy values
            "latency": 140,
            "energy_efficiency": 0.5,
            "accuracy": 0.98,
            "cached": False,
        },
    ),
    executor=GPTExecutor(model_id="text-davinci-002"),
)
_davinci_3 = Model(
    characteristics=ModelCharacteristics(
        hard_criteria=_gpt_hard_criteria,
        version=3,
        identity="davinci",
        soft_criteria={  # some dummy values
            "latency": 140,
            "energy_efficiency": 0.5,
            "accuracy": 0.99,
            "cached": False,
        },
    ),
    executor=GPTExecutor(model_id="text-davinci-003"),
)

MODELS = [_ada, _babbage, _curie, _davinci_1, _davinci_2, _davinci_3]
