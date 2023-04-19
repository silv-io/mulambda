from typing import Callable

from mulambda.context import model_injected
from mulambda.util import MULAMBDA


@model_injected()
def serverless_ml_function(model: Callable):
    print(model(MULAMBDA))


@model_injected()
def this_is_a_test(model: Callable):
    print(model("say this is a test"))


@model_injected()
def pass_through(model: Callable, text: str):
    print(f"sending {text} to model:")
    print(f"model response: {model(text)}")
    print("done.")
