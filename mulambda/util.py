import uuid
from typing import Union

from redis import asyncio as aioredis

from mulambda.config import settings

MULAMBDA = "\u03bc\u03bb"


def short_uid():
    return str(uuid.uuid4().hex[:8])


Number = Union[int, float]


async def get_redis():
    redis = await aioredis.from_url(
        f"redis://{settings.network.redis}{settings.network.base}"
    )
    try:
        yield redis
    finally:
        redis.close()
        await redis.wait_closed()
