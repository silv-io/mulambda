from fastapi import FastAPI
from ray import serve
from ray.serve.handle import RayServeDeploymentHandle
from starlette.requests import Request

app = FastAPI()


@serve.deployment
@serve.ingress(app)
class MulambdaIngress:
    matcher: RayServeDeploymentHandle

    def __init__(self, matcher: RayServeDeploymentHandle):
        self.matcher = matcher

    @app.get("/{name}")
    async def test(self, request: Request):
        return await request.json()
