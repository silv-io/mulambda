import abc
import logging

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
    def _pre_infer(self):
        LOG.debug("handling pre_infer...")
        return

    def _infer(self, input_data):
        LOG.debug("handling infer...")
        return input_data

    def _post_infer(self):
        LOG.debug("handling post_infer...")
        return
