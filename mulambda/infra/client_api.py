from typing import Dict

import httpx

from mulambda.util import get_metadata_server


async def get_model(
    required: Dict, desired: Dict, ranges: Dict, selector_url: str
) -> (str, Dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            selector_url,
            json={
                "required": required,
                "desired": desired,
                "ranges": ranges,
            },
        )
    print(f"Selected model: {response.json()}")
    traits = response.json()["model"]
    return (
        f"http://{response.json()['endpoint']}:{traits['port']}{traits['path']}",
        traits,
    )


async def send_model_data_delay(
    model_traits: Dict, client_id: str, rtt: int, data_size: int
):
    model_id = model_traits["id"]
    net_latency = model_traits["latencies"][client_id]
    metadata = get_metadata_server()
    mdd = (rtt - net_latency) / data_size
    await metadata.hset(model_id, "mdd", mdd)
