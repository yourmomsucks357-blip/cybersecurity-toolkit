import os, requests

def fetch_headlines():
    api_key = os.environ.get("NEWSAPI_KEY", "")
    if not api_key:
        print("Set NEWSAPI_KEY environment variable first")
        return
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    r = requests.get(url)
    if r.status_code == 200:
        for article in r.json()["articles"]:
            print(article["title"])
    else:
        print(f"Error: {r.status_code}")

if __name__ == "__main__":
    fetch_headlines()

