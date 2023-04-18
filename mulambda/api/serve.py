from typer import Typer

from mulambda.api.example import serverless_ml_function
from mulambda.context import global_context
from mulambda.models.registry import Model
from mulambda.openai.executor import OpenAIModelLister

app = Typer()


@app.command()
def main():
    global_context.model_registry.register_model(Model())
    serverless_ml_function()


@app.command("probe")
def probe():
    global_context.model_registry.register_model(Model(executor=OpenAIModelLister()))
    serverless_ml_function()
