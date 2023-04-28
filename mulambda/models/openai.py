import abc

import openai

from mulambda.config import settings
from mulambda.infra.base_model import BaseModel


class OpenAiModel(BaseModel, abc.ABC):
    openai_api_key: str
    openai_org_id: str
    model_id: str | None

    def __init__(self, model_id: str | None = None):
        super().__init__()
        self.openai_org_id = settings.openai_org_id
        self.openai_api_key = settings.openai_api_key
        self.model_id = model_id
        openai.api_key = self.openai_api_key
        openai.organization = self.openai_org_id


class OpenAiCompletionModel(OpenAiModel):
    def __init__(self, model_id: str = "text-ada-001"):
        super().__init__(model_id=model_id)

    def __call__(self, request: dict) -> str:
        return (
            openai.Completion.create(
                model=self.model_id,
                prompt=request["input"],
                max_tokens=settings.openai_max_tokens,
                temperature=settings.openai_temperature,
            )
            .choices[0]
            .text
        )
