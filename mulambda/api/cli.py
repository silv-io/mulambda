import ray
from typer import Typer

from mulambda.infra.selector import ModelSelector
from mulambda.infra.traits import ModelTraits
from mulambda.models.translator import TranslatorDeployment

app = Typer()


@app.command()
def main():
    print("test")


@app.command("serve")
def _serve():
    traits_1 = ModelTraits(
        identity="trans_1",
        model_type="translation",
        input_type="text",
        output_type="text",
        latency=100,
        accuracy=0.9,
    )
    traits_2 = ModelTraits(
        identity="trans_2",
        model_type="translation",
        input_type="text",
        output_type="text",
        latency=10,
        accuracy=0.5,
    )
    translator_1 = TranslatorDeployment.bind()
    translator_2 = TranslatorDeployment.bind()
    models = [(traits_1, translator_1), (traits_2, translator_2)]
    selector = ModelSelector.bind(models)
    # ingress = MulambdaIngress.bind(selector)
    ray.serve.run(selector)
    # TODO add a way to exit the server
    while True:
        # make sure the main thread doesn't exit
        pass
