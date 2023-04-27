from ray import serve
from transformers import pipeline

from mulambda.infra.base_model import BaseModel


@serve.deployment
class Translator(BaseModel):
    def __init__(self):
        super().__init__()
        # Load model
        self.model = pipeline("translation_en_to_fr", model="t5-small")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation

    # TODO make proper model for this
    def __call__(self, request: dict) -> str:
        return self.translate(request["input"])
