import abc
from typing import Any, TypedDict

ModelInput = TypedDict("ModelInput", {"input": Any})


class BaseModelBackend(abc.ABC):
    @abc.abstractmethod
    def __call__(self, request: ModelInput) -> Any:
        pass
