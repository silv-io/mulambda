import uuid
from typing import Union

MULAMBDA = "\u03bc\u03bb"

REDIS_PREFIX = "mulambda:"
REDIS_MODELS = REDIS_PREFIX + "models"
REDIS_CLIENTS = REDIS_PREFIX + "clients"
REDIS_LATENCIES = REDIS_PREFIX + "latencies"


def short_uid():
    return str(uuid.uuid4().hex[:8])


Number = Union[int, float]
