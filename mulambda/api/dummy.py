import asyncio
import collections
import random
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from mulambda.config import settings

app = FastAPI()

running_on = settings.dummy.node.id
concurrent_requests = 0
sem = asyncio.Semaphore()

recent_confidences = collections.deque(maxlen=10)
avg_sem = asyncio.Semaphore()


class ModelInput(BaseModel):
    feature: int
    inputs: List


def calculate_delay(model_input: ModelInput, concurrency: int) -> float:
    base_delay = settings.dummy.delay.base / 1000
    input_size = len(model_input.inputs)
    size_impact = settings.dummy.delay.size_impact
    concurrency_impact = settings.dummy.delay.concurrency_impact
    jitter = random.uniform(0, settings.dummy.delay.max_jitter / 1000)
    return (
        base_delay
        + input_size * size_impact
        + concurrency * concurrency_impact
        + jitter
    )


def calculate_confidence(model_input: ModelInput) -> float:
    confidences = settings.dummy.features.max_confidences
    try:
        base_confidence = confidences[model_input.feature]
    except IndexError:
        return 0.0

    set_size_impact = min(float(settings.dummy.features.set_size_impact), 1.0)
    set_size = len(confidences)
    if set_size == 0:
        return 0.0
    else:
        return base_confidence / set_size**set_size_impact


async def update_running_avg(confidence: float):
    global recent_confidences
    async with avg_sem:
        recent_confidences.append(confidence)
        average = sum(recent_confidences) / len(recent_confidences)
    return average


async def simulate_load(model_input: ModelInput) -> float:
    global concurrent_requests
    try:
        async with sem:
            delay = calculate_delay(model_input, concurrent_requests)
            concurrent_requests += 1
        print(f"Delaying for {delay} seconds")
        await asyncio.sleep(delay)
        confidence = calculate_confidence(model_input)
        print(f"Got confidence {confidence}")
        return calculate_confidence(model_input)
    finally:
        async with sem:
            concurrent_requests -= 1


@app.post("/")
async def read_root(model_input: ModelInput):
    confidence = await simulate_load(model_input)
    avg = await update_running_avg(confidence)
    return {
        "received": model_input.inputs,
        "confidence": confidence,
        "avg": avg,
        "node": running_on,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
