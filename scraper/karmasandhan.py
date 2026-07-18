import requests
from bs4 import BeautifulSoup

API_URL = "https://www.karmasandhan.com/wp-json/wp/v2/posts?per_page=10"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def html_to_text(html):
    return BeautifulSoup(html, "html.parser").get_text("\n", strip=True)


def get_latest_news():

    news = []

    try:

        response = requests.get(API_URL, headers=HEADERS, timeout=20)
        response.raise_for_status()

        posts = response.json()

        for post in posts:

            title = html_to_text(post["title"]["rendered"]).strip()

            content = html_to_text(post["content"]["rendered"]).strip()

            if len(content) < 100:
                continue

            news.append({
                "title": title,
                "content": content,
                "description": content[:500],
                "url": post["link"],
                "date": post["date"][:10]
            })

    except Exception as e:
        print("Karmasandhan Error:", e)

    return news
