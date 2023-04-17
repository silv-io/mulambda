from mulambda.models.registry import ModelRegistry


class MuLambdaContext:
    model_registry: ModelRegistry

    def __init__(self, model_registry: ModelRegistry = None):
        self.model_registry = model_registry or ModelRegistry()


# TODO look how to inject the context
global_context = MuLambdaContext()


def model_injected(hard_criteria=None, weights=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # TODO here we should select the model to inject
            model = global_context.model_registry.receive_model(hard_criteria, weights)
            return func(model.executor, *args, **kwargs)

        return wrapper

    return decorator
