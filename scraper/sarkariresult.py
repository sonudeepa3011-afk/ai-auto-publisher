import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

BASE_URL = "https://www.sarkariresult.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

KEYWORDS = [
    "result",
    "admit card",
    "answer key"
]


def get_page_content(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        paragraphs = []

        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if len(text) > 20:
                paragraphs.append(text)

        if len(paragraphs) < 3:
            text = soup.get_text("\n", strip=True)
            return text[:12000]

        return "\n".join(paragraphs)

    except Exception:
        return ""


def get_latest_news():

    news = []

    try:

        r = requests.get(BASE_URL, headers=HEADERS, timeout=20)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        seen = set()

        for a in soup.find_all("a"):

            title = a.get_text(" ", strip=True)

            if len(title) < 10:
                continue

            title_lower = title.lower()

            if not any(keyword in title_lower for keyword in KEYWORDS):
                continue

            href = a.get("href")

            if not href:
                continue

            url = urljoin(BASE_URL, href)

            if url in seen:
                continue

            seen.add(url)

            content = get_page_content(url)

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
        print("Sarkari Result Error:", e)

    return news
