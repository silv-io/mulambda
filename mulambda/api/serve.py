from typer import Typer

from mulambda.api.example import serverless_ml_function, this_is_a_test
from mulambda.context import global_context
from mulambda.models.registry import Model
from mulambda.openai.executor import GPTExecutor, OpenAIModelLister

app = Typer()


@app.command()
def main():
    global_context.model_registry.register_model(Model())
    serverless_ml_function()


@app.command("probe")
def probe():
    global_context.model_registry.register_model(Model(executor=GPTExecutor()))
    this_is_a_test()


@app.command("list")
def list():
    global_context.model_registry.register_model(Model(executor=OpenAIModelLister()))
    serverless_ml_function()
