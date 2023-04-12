import abc


class ModelInferencer(abc.ABC):
    def __init__(self):
        pass

    def infer(self, input_data):
        raise NotImplementedError()


