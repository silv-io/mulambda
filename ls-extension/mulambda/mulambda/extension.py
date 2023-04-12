import json
import logging
import numpy as np

from localstack.extensions.api import Extension, http, aws
from localstack.utils.aws import aws_stack
from localstack.http.dispatcher import Handler, ResultValue
from localstack.http import Request

LOG = logging.getLogger(__name__)

sagemaker_client = aws_stack.create_external_boto_client("sagemaker")
runtime_client = aws_stack.create_external_boto_client("sagemaker-runtime")
s3_client = aws_stack.create_external_boto_client("s3")


class MuLambdaExtension(Extension):
    name = "mulambda"
    HANDLED_MODELS = ["mnist"]
    EXTENSION_PATH = "/opt/code/extensions/mulambda"

    def on_extension_load(self):
        LOG.info("%r loading models: %r", self.name, self.HANDLED_MODELS)

    def on_platform_ready(self):
        s3_client.create_bucket(Bucket="mulambda-models")
        for model in self.HANDLED_MODELS:
            s3_client.upload_file(f"{self.EXTENSION_PATH}/mulambda/data/models/{model}.tar.gz",
                                  "mulambda-models", f"{model}.tar.gz")
            sagemaker_client.create_model(ModelName=f"mulambda-{model}",
                                          ExecutionRoleArn="arn:aws:iam::0000000000000:role/sagemaker-role",
                                          PrimaryContainer={
                                              "Image": "763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.5.0-cpu-py3",
                                              "ModelDataUrl": f"s3://mulambda-models/{model}.tar.gz"})
            sagemaker_client.create_endpoint_config(EndpointConfigName=f"mulambda-{model}-config",
                                                    ProductionVariants=[{
                                                        "ModelName": f"mulambda-{model}",
                                                        "InitialInstanceCount": 1,
                                                        "InstanceType": "ml.m5.large",
                                                        "VariantName": "AllTraffic"
                                                    }])
            sagemaker_client.create_endpoint(EndpointName=f"mulambda-{model}-endpoint",
                                             EndpointConfigName=f"mulambda-{model}-config")

    def update_gateway_routes(self, router: http.Router[http.RouteHandler]):
        router.add("/mulambda", MulambdaHandler())

    def update_request_handlers(self, handlers: aws.CompositeHandler):
        pass

    def update_response_handlers(self, handlers: aws.CompositeResponseHandler):
        pass


class MulambdaHandler(Handler):
    def on_post(self, request: Request):
        return self.__call__(request)

    def __call__(self, request: Request, **kwargs) -> ResultValue:
        data = json.loads(request.data)
        if "model" not in data:
            return {"error": "model not specified"}
        model = data["model"]
        response = runtime_client.invoke_endpoint(EndpointName=f"mulambda-{model}-endpoint",
                                                  Body=json.dumps(data["inputs"]), Accept="application/json",
                                                  ContentType="application/json")
        match model:
            case "mnist":
                return {
                    "result": np.argmax(np.array(json.loads(response["Body"].read().decode("utf-8")), dtype=np.float32),
                                        axis=1).tolist()}
            case _:
                return {"error": "unknown model"}
