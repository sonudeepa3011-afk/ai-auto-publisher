import requests
from bs4 import BeautifulSoup

API_URL = "API_URL = "https://hindi.buddy4study.com/wp-json/wp/v2/posts?per_page=20&_embed""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://YOUR-WEBSITE/"
}


def clean_text(html):
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)


def get_latest_news():

    news = []

    try:

        session = requests.Session()
        session.headers.update(HEADERS)

        response = session.get(API_URL, timeout=30)
        response.raise_for_status()

        posts = response.json()

        for post in posts:

            title = clean_text(post["title"]["rendered"])
            content = clean_text(post["content"]["rendered"])
            excerpt = clean_text(post["excerpt"]["rendered"])

            if len(content) < 200:
                continue

            news.append({
                "title": title,
                "content": content,
                "description": excerpt if excerpt else content[:300],
                "url": post["link"],
                "date": post["date"][:10]
            })

            print("Found:", title)

    except Exception as e:

        print("API Error:", e)

    return news
