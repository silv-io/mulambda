import ray
from typer import Typer

from mulambda.infra.selector import ModelSelector
from mulambda.models.translator import Translator

app = Typer()


@app.command()
def main():
    print("test")


@app.command("serve")
def _serve():
    translator_1 = Translator.bind()
    translator_2 = Translator.bind()
    models = [translator_1, translator_2]
    selector = ModelSelector.bind(models)
    # ingress = MulambdaIngress.bind(selector)
    ray.serve.run(selector)
    # TODO add a way to exit the server
    while True:
        # make sure the main thread doesn't exit
        pass
