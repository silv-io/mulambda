from typing import Dict, Tuple

import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from mulambda.infra.selector import ModelSelector, get_selector

app = FastAPI()


class ModelRequirements(BaseModel):
    required: Dict[str, str]
    desired: Dict[str, float]
    ranges: Dict[str, Tuple[float, float]]


@app.post("/")
async def read_root(
    reqs: ModelRequirements, selector: ModelSelector = Depends(get_selector)
):
    return selector(reqs.dict())


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
