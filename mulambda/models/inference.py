import abc


class ModelInferencer(abc.ABC):
    def __init__(self):
        pass

    def _infer(self, input_data):
        raise NotImplementedError()

    def __call__(self, input_data):
        return self._infer(input_data)

