import asyncio

import httpx

from mulambda.config import settings
from mulambda.util import send_galileo_event


async def async_run():
    await send_galileo_event({"type": "start"})
    exp = settings.experiment
    if exp["client_scale"] <= 1:
        endpoints = [
            f"http://{exp['target']}.mulambda.svc.cluster.local/usecase/"
            f"{exp['usecase']}?amount={exp['amount']}&size={exp['size']}&exp_id={exp['id']}"
        ]
    else:
        endpoints = [
            f"http://{exp['target']}-{client}.mulambda.svc.cluster.local/usecase/"
            f"{exp['usecase']}?amount={exp['amount']}&size={exp['size']}&exp_id={exp['id']}"
            for client in range(1, exp["client_scale"] + 1)
        ]
    async with httpx.AsyncClient() as client:
        tasks = []
        for endpoint in endpoints:
            for _ in range(exp["iterations"]):
                tasks.append(client.post(endpoint))
        await asyncio.gather(*tasks)

    await send_galileo_event({"type": "end"})


def run():
    import asyncio

    asyncio.run(async_run())


if __name__ == "__main__":
    run()
