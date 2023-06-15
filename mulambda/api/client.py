import httpx

if __name__ == "__main__":
    request = {
        "input": "Hello World!",
        "required": {"type": "translation", "input": "text", "output": "text"},
        "desired": {"latency": -0.1, "accuracy": 1},
        "ranges": {"latency": (0, 100)},
    }

    response = httpx.post("http://127.0.0.1:8000/", json=request)
    french_text = response.text

    print(french_text)
