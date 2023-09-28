import json
import time
import uuid
from typing import Dict, Union

from redis.asyncio.client import Redis

from mulambda.config import settings

MULAMBDA = "\u03bc\u03bb"

MULAMBDA_PREFIX = "mulambda:"
MULAMBDA_MODELS = MULAMBDA_PREFIX + "models"
MULAMBDA_CLIENTS = MULAMBDA_PREFIX + "clients"
MULAMBDA_LATENCIES = MULAMBDA_PREFIX + "latencies"

GALILEO_CHANNEL = "galileo/events"
GALILEO_METRIC = "mulambda"

EXPERIMENT_CHANNEL = "exp/events"


def get_metadata_server() -> Redis:
    return Redis(
        host=f"{settings.network.redis}.{settings.network.base}",
        # host="localhost",
        encoding="utf-8",
        decode_responses=True,
    )


def get_galileo_server() -> Redis:
    return Redis(
        host=settings.galileo.redis.host,
        password=settings.galileo.redis.password,
        encoding="utf-8",
        decode_responses=True,
    )


async def send_galileo_event(
    event: Dict,
    metric: str = GALILEO_METRIC,
):
    print(f"Sending event to Galileo: {event}")
    galileo = get_galileo_server()
    await galileo.publish(
        GALILEO_CHANNEL, f"{time.time()} {metric} {json.dumps(event)}"
    )
    await galileo.close()


async def send_experiment_event(
    event: str,
):
    print(f"Sending experiment event to Galileo: {event}")
    galileo = get_galileo_server()
    await galileo.publish(EXPERIMENT_CHANNEL, event)
    await galileo.close()


def short_uid():
    return str(uuid.uuid4().hex[:8])


Number = Union[int, float]
