import logging

import httpx
import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from mulambda.config import settings

app = FastAPI()
LOG = logging.getLogger(__name__)


class AppInput(BaseModel):
    data: str


async def get_endpoint():
    selection_target = {
        "required": {
            "type": settings.client.model_type,
            "input": settings.client.input_type,
            "output": settings.client.output_type,
        },
        "desired": {
            "latency": settings.client.latency_weight,
            "accuracy": settings.client.accuracy_weight,
        },
        "ranges": {
            "latency": settings.client.latency_range,
        },
    }
    selector = f"http://{settings.network.selector}.{settings.network.base}"
    async with httpx.AsyncClient() as client:
        response = await client.post(selector, json=selection_target)
        LOG.debug(f"Selected model: {response.json()}")
        return f"http://{response.json()['endpoint']}"


@app.post("/")
async def read_root(app_input: AppInput, endpoint: str = Depends(get_endpoint)):
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=app_input.dict())
        return response.json()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
