import openai

from mulambda.config import settings
from mulambda.models.executor import ModelExecutor


class OpenAIExecutor(ModelExecutor):
    openai_api_key: str
    openai_org_id: str

    def __init__(self):
        self.openai_org_id = settings.openai_org_id
        self.openai_api_key = settings.openai_api_key
        openai.api_key = self.openai_api_key
        openai.organization = self.openai_org_id

        super().__init__()

    def _infer(self, input_data):
        NotImplementedError()


class OpenAIModelLister(OpenAIExecutor):
    def _infer(self, _):
        return openai.Model.list()


class GPTExecutor(OpenAIExecutor):
    def _infer(self, input_data):
        pass


class DallEExecutor(OpenAIExecutor):
    def _infer(self, input_data):
        pass
