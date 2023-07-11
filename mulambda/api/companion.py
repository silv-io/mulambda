import logging
import time

import httpx
import typer
from redis import Redis

from mulambda.config import settings

LOG = logging.getLogger(__name__)
app = typer.Typer()


def get_latency(client_id: str) -> int:
    start_time = time.perf_counter()

    # Your code or function to measure
    httpx.get(f"http://{client_id}.{settings.network.base}")

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return int(execution_time * 1000)


@app.command()
def register():
    r = Redis(
        host=f"{settings.network.redis}.{settings.network.base}",
        # host="localhost",
        encoding="utf-8",
        decode_responses=True,
    )
    model = settings.companion.model
    print(f"Registering model {model}")
    r.sadd("models", model.id)
    r.hset(model.id, mapping=model)
    while True:
        clients = r.smembers("clients")
        for client in clients:
            curr_latency = get_latency(client)
            print(f"Client {client} latency for model {model.id}: {curr_latency}")
            r.hset(model.id, "latency", curr_latency)
        time.sleep(30)


if __name__ == "__main__":
    app()
