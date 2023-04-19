from typer import Typer

from mulambda.api.example import pass_through, serverless_ml_function
from mulambda.context import global_context
from mulambda.models.registry import Model
from mulambda.openai.executor import OpenAIModelLister
from mulambda.openai.models import MODELS

app = Typer()


@app.command()
def main():
    global_context.model_registry.register_model(Model())
    serverless_ml_function()


@app.command("prompt")
def prompt(prompt_input: str):
    global_context.model_registry.register_model(MODELS[0])
    pass_through(prompt_input)


@app.command("list")
def list_models():
    global_context.model_registry.register_model(Model(executor=OpenAIModelLister()))
    serverless_ml_function()
