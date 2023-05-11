import httpx

if __name__ == "__main__":
    request = {
        "input": "This will get translated to French!",
        "required": {"type": "translation", "input": "text", "output": "text"},
        "desired": {"latency": -1, "accuracy": 1},
        "ranges": {"latency": (0, 500)},
    }

    response = httpx.post("http://127.0.0.1:8000/", json=request)
    french_text = response.text

    print(french_text)
