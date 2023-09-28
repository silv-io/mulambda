from mulambda.infra.selector import ModelSelector
from mulambda.infra.traits import (
    ModelTraits,
)


class TestSelection:
    def test_desired(self):
        models = [
            (
                ModelTraits(
                    "id_1",
                    "test",
                    "test",
                    "test",
                    10,
                    {"test_client": 40},
                    0.3,
                    "test",
                    80,
                ),
                "id_1",
            ),
            (
                ModelTraits(
                    "id_2",
                    "test",
                    "test",
                    "test",
                    100,
                    {"test_client": 40},
                    0.8,
                    "test",
                    80,
                ),
                "id_2",
            ),
            (
                ModelTraits(
                    "id_3",
                    "test",
                    "test",
                    "test",
                    1,
                    {"test_client": 401},
                    0.8,
                    "test",
                    80,
                ),
                "id_3",
            ),
            (
                ModelTraits(
                    "id_4",
                    "test",
                    "test",
                    "test",
                    15,
                    {"test_client": 40},
                    0.7,
                    "test",
                    80,
                ),
                "id_4",
            ),
        ]
        selector = ModelSelector()
        for model in models:
            selector.append(model)

        selected = selector(
            "test_client",
            {
                "required": {"type": "test", "input": "test", "output": "test"},
                "desired": {"accuracy": 1, "latency": 0},
                "data_length": 10,
            },
        )
        assert selected["model"]["id"] == "id_2"

        selected = selector(
            "test_client",
            {
                "required": {"type": "test", "input": "test", "output": "test"},
                "desired": {"accuracy": 0, "latency": -1},
                "data_length": 10,
            },
        )
        assert selected["model"]["id"] == "id_1"

        selected = selector(
            "test_client",
            {
                "required": {"type": "test", "input": "test", "output": "test"},
                "desired": {"accuracy": 0, "latency": -1},
                "data_length": 100,
            },
        )
        assert selected["model"]["id"] == "id_3"

        selected = selector(
            "test_client",
            {
                "required": {"type": "test", "input": "test", "output": "test"},
                "desired": {"accuracy": 0.5, "latency": -0.5},
                "data_length": 10,
            },
        )
        assert selected["model"]["id"] == "id_4"
