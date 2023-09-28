import asyncio
import logging
import time

import httpx

from mulambda.config import settings
from mulambda.util import (
    MULAMBDA_CLIENTS,
    MULAMBDA_MODELS,
    get_metadata_server,
    send_galileo_event,
)

LOG = logging.getLogger(__name__)


def get_latency(client_id: str) -> int:
    print(
        f"Getting latency between client {client_id}"
        f"and model {settings.companion.model.id}"
    )
    start_time = time.perf_counter()

    httpx.get(f"http://{client_id}.{settings.network.base}/perf")

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return int(execution_time * 1000)


async def async_run():
    model = settings.companion.model
    metadata = get_metadata_server()

    print(f"Registering model {model}")
    await asyncio.gather(
        metadata.sadd(MULAMBDA_MODELS, model.id),
        metadata.hset(f"{MULAMBDA_MODELS}:{model.id}", mapping=model),
    )

    while True:
        clients = await metadata.smembers(MULAMBDA_CLIENTS)
        for client_id in clients:
            curr_latency = get_latency(client_id)
            print(f"Client {client_id} latency for model {model.id}: {curr_latency}")
            await asyncio.gather(
                metadata.hset(
                    f"{MULAMBDA_MODELS}:{model.id}",
                    f"latency:{client_id}",
                    str(curr_latency),
                ),
                send_galileo_event(
                    {
                        "type": "companion",
                        "client_id": client_id,
                        "model": model.id,
                        "latency": curr_latency,
                    },
                    "mulambda_companion",
                ),
            )
            await asyncio.sleep(5)


def run():
    asyncio.run(async_run())


if __name__ == "__main__":
    run()
