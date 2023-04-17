from typing import Callable

from mulambda.models.executor import ModelExecutor


class LocalExecutor(ModelExecutor):
    def __init__(self, model: Callable):
        self.model = model
        super().__init__()

    def _infer(self, input_data):
        return self.model(input_data)
