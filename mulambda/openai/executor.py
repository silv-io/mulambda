import openai

from mulambda.config import settings
from mulambda.models.executor import ModelExecutor


class OpenAIExecutor(ModelExecutor):
    openai_api_key: str
    openai_org_id: str
    model_id: str | None

    def __init__(self, model_id: str | None = None):
        self.openai_org_id = settings.openai_org_id
        self.openai_api_key = settings.openai_api_key
        self.model_id = model_id
        openai.api_key = self.openai_api_key
        openai.organization = self.openai_org_id

        super().__init__()

    def _infer(self, input_data):
        NotImplementedError()


class OpenAIModelLister(OpenAIExecutor):
    def _infer(self, _):
        return openai.Model.list()


class GPTExecutor(OpenAIExecutor):
    def __init__(self, model_id: str = "text-ada-001"):
        super().__init__(model_id=model_id)

    def _infer(self, input_data):
        return openai.Completion.create(
            model=self.model_id,
            prompt=input_data,
            max_tokens=settings.openai_max_tokens,
            temperature=settings.openai_temperature,
        )

    def _post_infer(self, output_data):
        return output_data.choices[0].text


class DallEExecutor(OpenAIExecutor):
    def _infer(self, input_data):
        pass
