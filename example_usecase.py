from model_registry import IdentityInferencer, MODELS, Model


def model_injected(hard_criteria=None, weights=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # TODO here we should select the model to inject
            model = MODELS.receive_model(hard_criteria, weights)
            return func(model.inferencer, *args, **kwargs)

        return wrapper

    return decorator


@model_injected()
def serverless_ml_function(model):
    print(model.infer("Silvio"))


if __name__ == '__main__':
    MODELS.register_model(Model())
    serverless_ml_function()
