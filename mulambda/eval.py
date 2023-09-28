USECASES = {
    "scp": {
        "desired": {"latency": -1, "accuracy": 0},
    },
    "mda": {
        "desired": {"latency": 0, "accuracy": 1},
    },
    "psa": {
        "desired": {"latency": -0.5, "accuracy": 0.5},
    },
    "env": {
        "desired": [
            {"latency": -0.5, "accuracy": 0.5},
            {"latency": -0.2, "accuracy": 0.8},
            {"latency": 0, "accuracy": 1},
            {"latency": -0.8, "accuracy": 0.2},
            {"latency": -1, "accuracy": 0},
        ],
    },
}
