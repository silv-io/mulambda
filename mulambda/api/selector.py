from typing import Dict

import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from mulambda.infra.selector import ModelSelector, get_selector

app = FastAPI()


class ModelRequirements(BaseModel):
    required: Dict[str, str]
    desired: Dict[str, float]
    data_length: int


@app.post("/select/{client_id}")
async def select_for_client(
    client_id, reqs: ModelRequirements, selector: ModelSelector = Depends(get_selector)
):
    return selector(client_id, reqs.model_dump())


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
