import time

import httpx
import typer
from redis.client import Redis

from mulambda.config import settings

app = typer.Typer()


# def get_experiment_clients():
#     ctx = Context()
#     rds = ctx.create_redis()
#     g = init(rds)
#     return g['exp'], ctx['telemd']


@app.command()
def run():
    mulambda_redis = Redis(
        host=f"{settings.network.redis}.{settings.network.base}",
        # host="localhost",
        encoding="utf-8",
        decode_responses=True,
    )
    client_id = next(iter(mulambda_redis.smembers("clients")))

    # exp, telemd = get_experiment_clients()

    print("Unpausing telemd...")
    # telemd.start_telemd()
    print(f"Starting experiment {settings.experiment.name}...")
    # exp.start(
    #    name=config.exp_name,
    #    creator=config.creator,
    #    metadata=metadata)
    print("Sleeping for 1 second...")
    time.sleep(1)

    httpx.post(
        f"http://{client_id}.{settings.network.base}", json={"inputs": [1, 2, 3]}
    )

    print("Pausing telemd...")
    # telemd.stop_telemd()
    print("Stopping experiment...")
    # exp.stop()
    print("Experiment finished.")


if __name__ == "__main__":
    app()
