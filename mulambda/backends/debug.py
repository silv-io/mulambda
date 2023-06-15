import time
from typing import Any

import numpy as np

from mulambda.infra.base_model import BaseModelBackend, ModelInput
from mulambda.util import short_uid


class LatencyModel(BaseModelBackend):
    mu: float
    sigma: float

    def __init__(self, mu: int = 100, sigma: int = 20):
        super().__init__()
        self.mu = mu
        self.sigma = sigma

    def _calculate_random_latency(self):
        return np.random.normal(self.mu, self.sigma)

    def __call__(self, request: ModelInput) -> Any:
        latency = self._calculate_random_latency()
        time.sleep(latency / 1000)
        return request["input"]


class IdentityModel(BaseModelBackend):
    identity: str

    def __init__(self, identity: str = None):
        super().__init__()
        self.identity = identity or short_uid()

    def __call__(self, request: ModelInput) -> Any:
        return f"[{self.identity}] received: {request['input']}"
