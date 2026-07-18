from datetime import datetime

from scraper.karmasandhan import get_latest_news as karmasandhan
from scraper.Sarkari Result import get_latest_news as sarkari result

from duplicate import is_duplicate
from gemini_ai import generate_news
from wordpress import create_draft


def main():

    print("=" * 70)
    print("AI NEWS AUTOMATION STARTED")
    print("=" * 70)

    news_list = []

    # karmasandhan 
    try:
        print("\nFetching karmasandhan News...")
        ranchi = ranchi_news()
        print(f"karmasandhan : {len(ranchi)} News")
        news_list.extend(ranchi)
    except Exception as e:
        print("karmasandhan  Error:", e)

    # Sarkari Result
    try:
        print("\nFetching Sarkari Result  News...")
        avenue = avenue_news()
        print(f"Sarkari Result : {len(avenue)} News")
        news_list.extend(avenue)
    except Exception as e:
        print("Sarkari Result  Error:", e)

    if not news_list:
        print("\nNo News Found.")
        return

    print(f"\nTotal Collected News: {len(news_list)}")

    # -------------------------
    # Today's News Only
    # -------------------------

    today = datetime.now().strftime("%Y-%m-%d")

    unique_urls = set()
    filtered_news = []

    for news in news_list:

        if news.get("date") != today:
            continue

        if news["url"] in unique_urls:
            continue

        unique_urls.add(news["url"])
        filtered_news.append(news)

    news_list = filtered_news

    print(f"Today's Unique News: {len(news_list)}")

    if not news_list:
        print("No Today's News Found.")
        return

    # Testing Limit
    # Remove this later if you want
    news_list = news_list[:10]

    created = 0

    for index, news in enumerate(news_list, start=1):

        print("\n" + "=" * 70)
        print(f"Processing News {index}")
        print("=" * 70)

        title = news["title"]
        content = news["content"]
        url = news["url"]

        print("Title :", title)
        print("URL   :", url)

        # Duplicate Check
        print("Checking Duplicate...")

        if is_duplicate(title):
            print("Already Exists. Skipping...")
            continue

        # Generate AI
        print("Generating AI Article...")

        try:
            result = generate_news(title, content)

        except Exception as e:

            print("Gemini Error:", e)

            if "429" in str(e):
                print("Gemini Quota Exceeded.")
                print("Stopping Automation.")
                break

            continue

        # WordPress Draft
        print("Creating Draft...")

        try:

            create_draft(
                result["title"],
                result["slug"],
                result["article"],
                result["meta_description"],
                result["comma_tags"]
            )

            created += 1

            print("Draft Created Successfully!")

        except Exception as e:
            print("WordPress Error:", e)

    print("\n" + "=" * 70)
    print("AUTOMATION COMPLETED")
    print("=" * 70)
    print(f"Draft Created : {created}")
    print(f"News Processed: {len(news_list)}")


if __name__ == "__main__":
    main()

