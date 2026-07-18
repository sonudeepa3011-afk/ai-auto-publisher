import os
import requests
from difflib import SequenceMatcher
from slugify import slugify

WP1_URL = os.getenv("WP1_URL")
WP1_USERNAME = os.getenv("WP1_USERNAME")
WP1_APP_PASSWORD = os.getenv("WP1_APP_PASSWORD")


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def is_duplicate(title):

    try:

        api = f"{WP1_URL}/wp-json/wp/v2/posts?per_page=100&status=any"

        response = requests.get(
            api,
            auth=(WP1_USERNAME, WP1_APP_PASSWORD),
            timeout=30
        )

        response.raise_for_status()

        posts = response.json()

        new_title = title.strip().lower()
        new_slug = slugify(title)

        for post in posts:

            old_title = (
                post.get("title", {})
                .get("rendered", "")
                .strip()
                .lower()
            )

            old_slug = post.get("slug", "").strip().lower()

            # Exact Title
            if new_title == old_title:
                print("Duplicate: Exact Title")
                return True

            # Exact Slug
            if new_slug == old_slug:
                print("Duplicate: Slug")
                return True

            # Similar Title
            if similarity(new_title, old_title) >= 0.85:
                print("Duplicate: Similar Title")
                return True

        return False

    except Exception as e:

        print("Duplicate Check Error:", e)

        return False
