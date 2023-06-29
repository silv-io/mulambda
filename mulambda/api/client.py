import logging
from typing import List

import httpx
import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from mulambda.config import settings

app = FastAPI()
LOG = logging.getLogger(__name__)


class TestInput(BaseModel):
    inputs: List


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
        print(f"Selected model: {response.json()}")
        traits = response.json()["model"]
        return f"http://{response.json()['endpoint']}:{traits['port']}{traits['path']}"


@app.post("/")
async def read_root(test_input: TestInput, endpoint: str = Depends(get_endpoint)):
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=test_input.dict())
        return response.json()


@app.post("/sim/")
async def read_sim(amount: int = 10):
    answers = []
    async with httpx.AsyncClient() as client:
        while amount > 0:
            amount -= 1
            test_input = TestInput(inputs=[1.0, 2.0, 3.0])
            endpoint = await get_endpoint()
            response = await client.post(endpoint, json=test_input.dict())
            answers.append(response.json())
    return answers


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
