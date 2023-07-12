import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import httpx
import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from redis import asyncio as aioredis

from mulambda.config import settings
from mulambda.util import REDIS_CLIENTS


@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_redis = await aioredis.from_url(
        f"redis://{settings.network.redis}.{settings.network.base}",
        # "redis://localhost:6379",
        encoding="utf-8",
        decode_responses=True,
    )
    await ml_redis.sadd(REDIS_CLIENTS, settings.client.id)

    yield

    ml_redis.sdel(REDIS_CLIENTS, settings.client.id)


app = FastAPI(lifespan=lifespan)
LOG = logging.getLogger(__name__)


class TestInput(BaseModel):
    inputs: List


async def get_dummy_endpoint():
    selection_target = {
        "required": {
            "type": "dummy",
            "input": "floatvector",
            "output": "floatvector",
        },
        "desired": {
            "latency": -0.1,
            "accuracy": 0.9,
        },
        "ranges": {
            "latency": [0, 1000],
        },
    }
    selector_url = (
        f"http://{settings.network.selector}.{settings.network.base}"
        f"/select/{settings.client.id}"
    )
    async with httpx.AsyncClient() as client:
        response = await client.post(selector_url, json=selection_target)
        print(f"Selected model: {response.json()}")
        traits = response.json()["model"]
        return f"http://{response.json()['endpoint']}:{traits['port']}{traits['path']}"


@app.post("/")
async def read_root(test_input: TestInput, endpoint: str = Depends(get_dummy_endpoint)):
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=test_input.model_dump())
        return response.json()


@app.post("/sim/")
async def read_sim(amount: int = 10):
    answers = []
    async with httpx.AsyncClient() as client:
        while amount > 0:
            amount -= 1
            test_input = TestInput(inputs=[1.0, 2.0, 3.0])
            endpoint = await get_dummy_endpoint()
            response = await client.post(endpoint, json=test_input.model_dump())
            answers.append(response.json())
    return answers


@app.get("/perf")
async def read_perf():
    return {"arrival": datetime.now().isoformat()}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
