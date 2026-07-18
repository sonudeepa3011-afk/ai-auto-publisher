import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_news(title, description):

    prompt = f"""
You are an expert Government Job, Result and Education News writer.

Create a completely unique SEO optimized article.

News Title:
{title}

News Content:
{description}

Rules:

1. Write in Simple English Easy to understand.
2. Keep words like Result, Admit Card, Recruitment, Notification, Apply Online, Last Date, Official Website, Exam Date in English.
3. Human written style.
4. Google Discover Friendly.
5. 800-1200 words.
6. Use H2 and H3 headings.
7. Short paragraphs.
8. Bullet points.
9. 5 SEO FAQs.
10. Short Conclusion.
11. Return clean HTML only.
12. No Markdown.

Return ONLY in this format:

TITLE:
...

SLUG:
...

META DESCRIPTION:
...

COMMA TAGS:
...

ARTICLE:
...
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 8192,
        },
    )

    text = response.text.strip()

    data = {
        "title": title,
        "slug": "",
        "meta_description": "",
        "comma_tags": "",
        "article": text,
    }

    try:
        data["title"] = text.split("TITLE:")[1].split("SLUG:")[0].strip()
        data["slug"] = text.split("SLUG:")[1].split("META DESCRIPTION:")[0].strip()
        data["meta_description"] = text.split("META DESCRIPTION:")[1].split("COMMA TAGS:")[0].strip()
        data["comma_tags"] = text.split("COMMA TAGS:")[1].split("ARTICLE:")[0].strip()
        data["article"] = text.split("ARTICLE:")[1].strip()

    except Exception:
        print("Warning: Gemini response format changed. Using raw article.")

    return data
