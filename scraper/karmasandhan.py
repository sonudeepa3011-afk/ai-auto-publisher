import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.karmasandhan.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_article_content(url):

    try:

        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        article = (
            soup.find("article")
            or soup.find("div", class_="td-post-content")
            or soup.find("div", class_="entry-content")
        )

        if not article:
            return ""

        paragraphs = []

        for p in article.find_all("p"):

            text = p.get_text(" ", strip=True)

            if len(text) > 20:
                paragraphs.append(text)

        return "\n".join(paragraphs)

    except Exception as e:
        print("Article Error:", e)
        return ""


def get_latest_news():

    news = []

    try:

        r = requests.get(BASE_URL, headers=HEADERS, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        seen = set()

        # Homepage ke saare article cards
        articles = soup.find_all("article")

        for article in articles:

            h2 = article.find(["h2", "h3"])

            if not h2:
                continue

            a = h2.find("a")

            if not a:
                continue

            title = a.get_text(" ", strip=True)

            url = urljoin(BASE_URL, a.get("href"))

            if url in seen:
                continue

            seen.add(url)

            content = get_article_content(url)

            if len(content) < 200:
                continue

            news.append({
                "title": title,
                "content": content,
                "description": content[:300],
                "url": url,
                "date": ""
            })

            print("Found:", title)

            if len(news) >= 20:
                break

    except Exception as e:

        print("Karmasandhan Error:", e)

    return news
