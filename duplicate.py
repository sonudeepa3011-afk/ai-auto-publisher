import os
import requests
from slugify import slugify

WP_URL = os.getenv("WP1_URL")
WP_USERNAME = os.getenv("WP1_USERNAME")
WP_APP_PASSWORD = os.getenv("WP1_APP_PASSWORD")


def is_duplicate(title):
    slug = slugify(title)

    response = requests.get(
        f"{WP1_URL}/wp-json/wp/v2/posts",
        params={
            "search": slug,
            "per_page": 10,
            "status": "draft,publish"
        },
        auth=(WP1_USERNAME, WP1_APP_PASSWORD),
        timeout=20
    )

    if response.status_code != 200:
        return False

    posts = response.json()

    title = title.strip().lower()

    for post in posts:

        wp_title = post["title"]["rendered"].strip().lower()

        if wp_title == title:
            return True

        if post["slug"] == slug:
            return True

    return False
