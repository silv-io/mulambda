from typing import Callable

from mulambda.context import global_context, model_injected
from mulambda.models.registry import Model


@model_injected()
def serverless_ml_function(model: Callable):
    print(model("Silvio"))


if __name__ == "__main__":
    global_context.model_registry.register_model(Model())
    serverless_ml_function()
