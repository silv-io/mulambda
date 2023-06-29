import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ModelInput(BaseModel):
    data: str


@app.post("/")
async def read_root(model_input: ModelInput):
    return f"received: {model_input.data}"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
