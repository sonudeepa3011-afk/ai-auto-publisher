import requests
from bs4 import BeautifulSoup

API_URL = "https://sarkariresult.com.cm/wp-json/wp/v2/posts?per_page=10"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_html(html):
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)


def get_latest_news():

    news = []

    try:

        response = requests.get(API_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()

        posts = response.json()

        for post in posts:

            title = clean_html(post["title"]["rendered"])
            content = clean_html(post["content"]["rendered"])
            excerpt = clean_html(post["excerpt"]["rendered"])

            if len(content) < 100:
                continue

            news.append({
                "title": title,
                "content": content,
                "description": excerpt,
                "url": post["link"],
                "date": post["date"][:10]
            })

    except Exception as e:
        print("Sarkari Result API Error:", e)

    return news
