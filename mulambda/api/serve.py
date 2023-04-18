from typer import Typer

from mulambda.util import MULAMBDA

app = Typer()


@app.command()
def hello():
    print(f"Hello {MULAMBDA}.")
