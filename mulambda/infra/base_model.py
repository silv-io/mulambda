import abc
from typing import Any, TypedDict

ModelInput = TypedDict("ModelInput", {"input": Any})


class BaseModelDeployment(abc.ABC):
    @abc.abstractmethod
    def __call__(self, request: ModelInput) -> Any:
        pass
