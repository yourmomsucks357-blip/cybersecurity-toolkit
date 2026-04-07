import requests
import base64

class AnthropicClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

    def chat(self, message, model="claude-sonnet-4-20250514", max_tokens=1024):
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": message}]
        }
        r = requests.post(self.url, json=payload, headers=self.headers)
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
        else:
            raise Exception(f"Anthropic error {r.status_code}: {r.text}")

    def chat_with_image(self, message, image_path, model="claude-sonnet-4-20250514", max_tokens=1024):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        
        ext = image_path.lower().split(".")[-1]
        media_type = {"png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg","gif":"image/gif","webp":"image/webp"}.get(ext, "image/png")
        
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": encoded}},
                    {"type": "text", "text": message}
                ]
            }]
        }
        r = requests.post(self.url, json=payload, headers=self.headers)
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
        else:
            raise Exception(f"Anthropic error {r.status_code}: {r.text}")

if __name__ == "__main__":
    import sys
    key = sys.argv[1] if len(sys.argv) > 1 else input("Anthropic API key: ")
    client = AnthropicClient(key)
    print(client.chat("Hello, are you working?"))

