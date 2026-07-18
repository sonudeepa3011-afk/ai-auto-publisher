import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://hindi.buddy4study.com/"

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
            or soup.find("div", class_="entry-content")
            or soup.find("main")
        )

        if not article:
            return ""

        paragraphs = []

        for p in article.find_all("p"):

            text = p.get_text(" ", strip=True)

            if len(text) > 25:
                paragraphs.append(text)

        return "\n".join(paragraphs)

    except Exception as e:

        print("Buddy4Study Article Error:", e)
        return ""


def get_latest_news():

    news = []

    try:

        r = requests.get(BASE_URL, headers=HEADERS, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        seen = set()

        for a in soup.find_all("a", href=True):

            href = urljoin(BASE_URL, a["href"])

            if BASE_URL not in href:
                continue

            if href == BASE_URL:
                continue

            if href in seen:
                continue

            seen.add(href)

            title = a.get_text(" ", strip=True)

            if len(title) < 15:
                continue

            content = get_article_content(href)

            if len(content) < 300:
                continue

            news.append({
                "title": title,
                "content": content,
                "description": content[:300],
                "url": href,
                "date": ""
            })

            print("Found:", title)

            if len(news) >= 20:
                break

    except Exception as e:

        print("Buddy4Study Error:", e)

    return news
