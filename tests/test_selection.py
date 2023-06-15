from mulambda.infra.traits import (
    DesiredTraitWeights,
    ModelTraits,
    NormalizationRanges,
    RequiredTraits,
)


class TestSelection:
    def test_required(self):
        models = [
            ModelTraits(
                "id_1",
                "translation",
                "text",
                "text",
                100,
                0.9,
            ),
            ModelTraits(
                "id_2",
                "completion",
                "text",
                "text",
                100,
                0.9,
            ),
            ModelTraits(
                "id_3",
                "classification",
                "image",
                "text",
                100,
                0.9,
            ),
            ModelTraits(
                "id_4",
                "translation",
                "text",
                "text",
                100,
                0.9,
            ),
        ]

        req = RequiredTraits("translation", "text", "text")
        filtered = [model for model in models if model.hard_filter(req)]
        assert len(filtered) == 2
        assert filtered[0]["id"] == "id_1"

        req = RequiredTraits("classification", "image", "text")
        filtered = [model for model in models if model.hard_filter(req)]
        assert len(filtered) == 1
        assert filtered[0]["id"] == "id_3"

    def test_desired(self):
        models = [
            ModelTraits(
                "id_1",
                "translation",
                "text",
                "text",
                500,
                0.99,
            ),
            ModelTraits(
                "id_2",
                "translation",
                "text",
                "text",
                300,
                0.8,
            ),
            ModelTraits(
                "id_3",
                "translation",
                "text",
                "text",
                20,
                0.95,
            ),
            ModelTraits(
                "id_4",
                "translation",
                "text",
                "text",
                10,
                0.60,
            ),
        ]
        ranges = NormalizationRanges(latency=(0, 500))
        weights = DesiredTraitWeights(latency=-1, accuracy=1)

        minimum = min(models, key=lambda model: model.sort_key(weights, ranges))
        assert minimum["id"] == "id_3"

        weights = DesiredTraitWeights(latency=-1, accuracy=0)
        minimum = min(models, key=lambda model: model.sort_key(weights, ranges))
        assert minimum["id"] == "id_4"

        weights = DesiredTraitWeights(latency=0, accuracy=1)
        minimum = min(models, key=lambda model: model.sort_key(weights, ranges))
        assert minimum["id"] == "id_1"
