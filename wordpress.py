import os
import requests

WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")


def create_draft(title, slug, article, meta_description, comma_tags):

    url = f"{WP_URL}/wp-json/wp/v2/posts"

    final_content = f"""
{article}

<hr>

<h3>SEO Details</h3>

<p><strong>Meta Description:</strong></p>
<p>{meta_description}</p>

<p><strong>Comma Tags:</strong></p>
<p>{comma_tags}</p>
"""

    data = {
        "title": title,
        "slug": slug,
        "content": final_content,
        "status": "draft"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        auth=(WP_USERNAME, WP_APP_PASSWORD)
    )

    if response.status_code in [200, 201]:
        result = response.json()

        print("=" * 50)
        print("✅ Draft Created Successfully!")
        print(f"Post ID  : {result.get('id')}")
        print(f"Post URL : {result.get('link')}")
        print("=" * 50)

        return result

    print("=" * 50)
    print("❌ Failed to Create Draft")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    print("=" * 50)

    raise Exception("WordPress Draft Creation Failed")
