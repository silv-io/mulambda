from typing import Callable

from mulambda.context import model_injected
from mulambda.util import MULAMBDA


@model_injected()
def serverless_ml_function(model: Callable):
    print(model(MULAMBDA))


@model_injected()
def this_is_a_test(model: Callable):
    print(model("say this is a test"))
