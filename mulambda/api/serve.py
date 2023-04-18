from typer import Typer

from mulambda.api.example import serverless_ml_function
from mulambda.context import global_context
from mulambda.models.registry import Model

app = Typer()


@app.command()
def main():
    global_context.model_registry.register_model(Model())
    serverless_ml_function()
