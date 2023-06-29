import logging
import random
import time

import typer
from redis import Redis

from mulambda.config import settings

LOG = logging.getLogger(__name__)
app = typer.Typer()


def get_latency(client_id: str) -> int:
    # TODO get latency dynamically from client
    return 100 + random.randint(-10, 10)


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
        curr_latency = get_latency("client")
        print(f"Updating latency to {curr_latency}")
        r.hset(model.id, "latency", curr_latency)
        time.sleep(30)


if __name__ == "__main__":
    app()
