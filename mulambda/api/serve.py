from typer import Typer

app = Typer()


@app.command()
def hello():
    print("Hello World.")
