from ray import serve
from transformers import pipeline

from mulambda.infra.base_model import BaseModelDeployment, ModelInput


@serve.deployment
class TranslatorDeployment(BaseModelDeployment):
    def __init__(self, model_id: str = "translation_en_to_fr"):
        super().__init__()
        # Load model
        self.model = pipeline(model_id, model="t5-small")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation

    def __call__(self, request: ModelInput) -> str:
        return self.translate(request["input"])
