import logging
import random
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, List

import httpx
import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI
from pydantic import BaseModel

from mulambda.config import settings
from mulambda.eval import USECASES
from mulambda.infra.client_api import get_model
from mulambda.util import send_galileo_event


@asynccontextmanager
async def lifespan(app: FastAPI):
    # metadata = get_metadata_server()
    # await metadata.sadd(MULAMBDA_CLIENTS, settings.client.id)

    yield

    # await metadata.srem(MULAMBDA_CLIENTS, settings.client.id)


app = FastAPI(lifespan=lifespan)
LOG = logging.getLogger(__name__)


class TestInput(BaseModel):
    inputs: List


async def get_dummy_model():
    return await get_model(
        required={"type": "dummy", "input": "floatvector", "output": "floatvector"},
        desired={"latency": -0.1, "accuracy": 0.9},
        ranges={"latency": [0, 1000]},
        selector_url=(
            f"http://{settings.network.selector}.{settings.network.base}"
            f"/select/{settings.client.id}"
        ),
    )


async def post_traced(model: (str, Dict), data: Dict):
    endpoint = model[0]
    traits = model[1]
    trace = {
        "type": "request",
        "client_id": settings.client.id,
        "data": data,
        "endpoint": endpoint,
        "model_traits": traits,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, json=data)
    trace["elapsed"] = response.elapsed.total_seconds()
    await send_galileo_event(trace)
    return response.json()


@app.post("/")
async def read_root(
    test_input: TestInput, model: (str, Dict) = Depends(get_dummy_model)
):
    return await post_traced(model, test_input.model_dump())


def generate_random_input(size: int):
    return [round(random.random() * 100, 2) for _ in range(size)]


async def simulate_multiple(amount: int, size: int):
    while amount > 0:
        amount -= 1
        model = await get_dummy_model()
        response = await post_traced(model, {"inputs": generate_random_input(size)})
        print(response)


@app.post("/sim-dummy/")
async def read_sim(
    background_tasks: BackgroundTasks,
    amount: int = 100,
    size: int = 10,
):
    background_tasks.add_task(simulate_multiple, amount, size)
    return {"status": "ok", "amount": amount, "size": size}


async def batch_send(amount: int, size: int, desired: Dict):
    for _ in range(amount):
        model = await get_model(
            desired=desired,
            required={"type": "dummy", "input": "floatvector", "output": "floatvector"},
            ranges={"latency": [0, 1000]},
            selector_url=(
                f"http://{settings.network.selector}.{settings.network.base}"
                f"/select/{settings.client.id}"
            ),
        )
        await post_traced(model, {"inputs": generate_random_input(size)})


@app.post("/usecase/{usecase}")
async def sim_usecase(
    usecase: str, background_tasks: BackgroundTasks, amount: int = 100, size: int = 10
):
    match usecase:
        case "scp" | "mda" | "psa":
            background_tasks.add_task(
                batch_send,
                amount,
                size,
                USECASES[usecase],
            )
        case "env":
            # TODO
            return "stream test"


@app.get("/perf")
async def read_perf():
    return {"arrival": datetime.now().isoformat()}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
