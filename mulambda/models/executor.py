import abc
import logging
import time

import numpy as np

from mulambda.util import short_uid

LOG = logging.getLogger(__name__)


class ModelExecutor(abc.ABC):
    def __init__(self):
        # TODO think about setup
        pass

    def _pre_infer(self, input_data):
        # TODO input handling
        return input_data

    def _infer(self, input_data):
        raise NotImplementedError()

    def _post_infer(self, output_data):
        # TODO output handling
        return output_data

    def __call__(self, input_data):
        handled_input = self._pre_infer(input_data)
        output_data = self._infer(handled_input)
        handled_output = self._post_infer(output_data)
        return handled_output


class IdentityExecutor(ModelExecutor):
    def __init__(self, identity: str = None):
        self.identity = identity or short_uid()
        super().__init__()

    def _infer(self, input_data):
        return f"[{self.identity}] received: {input_data}"


# TODO add sleep timers and debug input and output handling
class DebugExecutor(ModelExecutor):
    # mean and standard deviation of latency
    mu_latency: int
    sigma_latency: int

    def __init__(self, mu_latency: int = 100, sigma_latency: int = 20):
        super().__init__()

    def _calculate_random_latency(self):
        return np.random.normal(self.mu_latency, self.sigma_latency)

    def _pre_infer(self, input_data):
        LOG.debug("handling pre_infer...")
        return input_data

    def _infer(self, input_data):
        LOG.debug("handling infer...")
        wait_time = self._calculate_random_latency()
        LOG.debug(f"waiting for {wait_time} ms")
        time.sleep(wait_time / 1000)
        return input_data

    def _post_infer(self, output_data):
        LOG.debug("handling post_infer...")
        return output_data
