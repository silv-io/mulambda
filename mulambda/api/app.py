from contextlib import asynccontextmanager

import httpx
import uvicorn
from fastapi import FastAPI

from mulambda.backends.debug import IdentityModel
from mulambda.infra.selector import ModelSelector
from mulambda.infra.traits import ModelTraits

selector = ModelSelector([])


@asynccontextmanager
async def lifespan(_):
    # Load the ML model

    backend_a = IdentityModel("id_1")
    traits_a = ModelTraits(
        "id_1",
        "translation",
        "text",
        "text",
        500,
        0.99,
    )

    backend_b = IdentityModel("id_2")
    traits_b = ModelTraits(
        "id_2",
        "translation",
        "text",
        "text",
        10,
        0.6,
    )
    models = [(traits_a, backend_a), (traits_b, backend_b)]
    selector.append(models[0])
    selector.append(models[1])

    yield
    # Clean up the ML models and release the resources
    print("bye bye")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return httpx.get("http://dummy-backend.default.svc.cluster.local").text


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
