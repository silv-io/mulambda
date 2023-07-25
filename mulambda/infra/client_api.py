from typing import Dict

import httpx


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
