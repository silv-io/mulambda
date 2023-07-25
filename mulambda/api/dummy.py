import asyncio
import random
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from mulambda.config import settings

app = FastAPI()


class ModelInput(BaseModel):
    inputs: List


async def simulate_load():
    wait_time = random.normalvariate(
        float(settings.dummy.mean) / 1000, float(settings.dummy.std) / 1000
    )
    print(f"Simulating load for {wait_time} seconds")
    # TODO cpu load
    await asyncio.sleep(wait_time)
    return


@app.post("/")
async def read_root(model_input: ModelInput):
    await simulate_load()
    return {"received": model_input.inputs}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
