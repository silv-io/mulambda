import httpx

from mulambda.util import send_galileo_event


async def async_run():
    await send_galileo_event({"type": "start"})
    httpx.post(
        "http://experiment-client.mulambda.svc.cluster.local/sim-dummy/?amount=100&size=10"
    )
    await send_galileo_event({"type": "end"})


def run():
    import asyncio

    asyncio.run(async_run())


if __name__ == "__main__":
    run()
