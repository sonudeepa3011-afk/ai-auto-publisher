from datetime import datetime

from scraper.karmasandhan import get_latest_news as karmasandhan_news
from scraper.sarkariresult import get_latest_news as sarkariresult_news
from scraper.buddy4study import get_latest_news as buddy_news

from duplicate import is_duplicate
from gemini_ai import generate_news
from wordpress import create_draft


def main():

    print("=" * 70)
    print("AI NEWS AUTOMATION STARTED")
    print("=" * 70)

    news_list = []

    # ==========================
    # Karmasandhan
    # ==========================
    try:
        print("\nFetching Karmasandhan News...")
        karmasandhan = karmasandhan_news()[:10]
        print(f"Karmasandhan : {len(karmasandhan)} News")
        news_list.extend(karmasandhan)

    except Exception as e:
        print("Karmasandhan Error:", e)

    # ==========================
    # Sarkari Result
    # ==========================
    try:
        print("\nFetching Sarkari Result News...")
        sarkari = sarkariresult_news()[:10]
        print(f"Sarkari Result : {len(sarkari)} News")
        news_list.extend(sarkari)

    except Exception as e:
        print("Sarkari Result Error:", e)

    # ==========================
    # Buddy4Study
    # ==========================
    try:
        print("\nFetching Buddy4Study News...")
        buddy = buddy_news()[:10]
        print(f"Buddy4Study : {len(buddy)} News")
        news_list.extend(buddy)

    except Exception as e:
        print("Buddy4Study Error:", e)

    # ==========================

    if not news_list:
        print("\nNo News Found.")
        return

    print(f"\nTotal Collected News : {len(news_list)}")

    today = datetime.now().strftime("%Y-%m-%d")

    unique_urls = set()
    filtered_news = []

    for news in news_list:

        if news.get("date") not in ("", today):
            continue

        if news["url"] in unique_urls:
            continue

        unique_urls.add(news["url"])
        filtered_news.append(news)

    news_list = filtered_news

    print(f"Today's Unique News : {len(news_list)}")

    if not news_list:
        print("No Today's News Found.")
        return

    # Testing
    # news_list = news_list[:10]

    created = 0
    skipped = 0
    failed = 0

    for index, news in enumerate(news_list, start=1):

        print("\n" + "=" * 70)
        print(f"Processing {index}/{len(news_list)}")
        print("=" * 70)

        title = news["title"]
        content = news["content"]
        url = news["url"]

        print("Title :", title)
        print("URL   :", url)

        # Duplicate
        if is_duplicate(title):
            print("Duplicate Found. Skipped.")
            skipped += 1
            continue

        # Gemini
        try:

            print("Generating AI Article...")

            result = generate_news(title, content)

        except Exception as e:

            print("Gemini Error:", e)

            if "429" in str(e):
                print("Gemini Daily Quota Exceeded.")
                break

            failed += 1
            continue

        # WordPress
        try:

            print("Creating Draft...")

            create_draft(
                result["title"],
                result["slug"],
                result["article"],
                result["meta_description"],
                result["comma_tags"]
            )

            created += 1

            print("Draft Created Successfully.")

        except Exception as e:

            print("WordPress Error:", e)
            failed += 1

    print("\n" + "=" * 70)
    print("AUTOMATION COMPLETED")
    print("=" * 70)

    print(f"Fetched    : {len(news_list)}")
    print(f"Created    : {created}")
    print(f"Skipped    : {skipped}")
    print(f"Failed     : {failed}")


if __name__ == "__main__":
    main()
