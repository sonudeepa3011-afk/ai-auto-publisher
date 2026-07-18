import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")


def generate_news(title, description):

    prompt = f"""
You are a professional Goverment job Expert and SEO Content Writer.

Write a 100% unique, plagiarism-free, Google Discover friendly news article.

News Title:
{title}

News Description:
{description}

Requirements:

1. Write the article in Hindi (Devanagari).
2. Keep important words like Result, Admit Card, Recruitment, Notification, Apply Online, Last Date, Official Website, Exam Date, Launch, Price etc. in English.
3. Use simple human-like language.
4. Use H2 and H3 headings.
5. Keep paragraphs short (2-3 lines).
6. Use bullet points where needed.
7. Include only verified facts from the given news.
8. Add 5 SEO-friendly FAQs.
9. Add a short conclusion.
10. Write 800-1200 words.
11. Output article in clean HTML only.
12. Do not use Markdown.

Return output exactly in this format:

TITLE:
(SEO Friendly Title)

SLUG:
(English only, lowercase, hyphen separated)

META DESCRIPTION:
(150-160 characters)

COMMA TAGS:
(12 SEO Friendly comma separated tags)

ARTICLE:
(Complete HTML Article)
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    data = {
        "title": "",
        "slug": "",
        "meta_description": "",
        "comma_tags": "",
        "article": ""
    }

    try:

        data["title"] = text.split("TITLE:")[1].split("SLUG:")[0].strip()

        data["slug"] = text.split("SLUG:")[1].split("META DESCRIPTION:")[0].strip()

        data["meta_description"] = text.split("META DESCRIPTION:")[1].split("COMMA TAGS:")[0].strip()

        data["comma_tags"] = text.split("COMMA TAGS:")[1].split("ARTICLE:")[0].strip()

        data["article"] = text.split("ARTICLE:")[1].strip()

    except Exception:
        data["article"] = text

    return data
