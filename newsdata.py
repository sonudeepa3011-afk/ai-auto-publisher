import os
import requests

BASE_URL = "https://newsdata.io/api/1/news"

def get_latest_news():
    api_key = os.getenv("NEWSDATA_API_KEY")

    params = {
        "apikey": api_key,
        "country": "in",
        "language": "en"
    }

    response = requests.get(BASE_URL, params=params, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"NewsData API Error: {response.status_code} - {response.text}"
        )

    data = response.json()

    if "results" not in data or not data["results"]:
        raise Exception("No news found.")

    return data["results"][0]
