import httpx

english_text = "Hello world!"

response = httpx.post("http://127.0.0.1:8000/", json={"input": english_text})
french_text = response.text

print(french_text)
