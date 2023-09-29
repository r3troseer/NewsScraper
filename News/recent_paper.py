from newspaper import build
from datetime import datetime, timedelta, timezone

dailypost_url = "https://dailypost.ng/hot-news/"
punch_url = "https://punchng.com/topics/news/"
the_nation_url = "https://thenationonlineng.net/news/"
tribune_url = "https://tribuneonlineng.com/category/top-news/"
vanguard_url = "https://www.vanguardngr.com/category/top-stories/"


def get_recent_articles(base_url, max_articles=5, max_age_days=2, max_retries=3):
    """
    Get recent articles from a news website.

    Args:
        base_url (str): The URL of the news website.
        max_articles (int): The maximum number of articles to retrieve.
        max_age_days (int): The maximum age (in days) of articles to consider.
        max_retries (int): The maximum number of retries for each article.

    Returns:
        list: A list of dictionaries containing article information.
    """
    # Build the newspaper with no caching.
    paper = build(base_url, memoize_articles=False)

    # Initialize a list to store dictionaries for each article.
    articles_list = []

    # Define the maximum age for articles (2 days ago from the current date by default).
    max_age = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    print(max_age)

    # Loop through the articles and collect the text and title of the first 10 articles published within the last 2 days by default.
    for article in paper.articles:
        if len(articles_list) >= max_articles:
            break  # Stop once 10 articles has been collected.

        retries = 0
        article_processed = (
            False  # Flag to track if the article has been successfully processed
        )
        while retries < max_retries:
            try:
                # Download and parse the article.
                article.download()
                article.parse()

                # Get the publication date of the article.
                published_date = article.publish_date
                print(published_date)

                # Check if the article is within the desired age limit.
                if published_date is not None and published_date >= max_age:
                    # Create a dictionary to store article information.
                    article_info = {
                        "title": article.title,
                        "text": article.text,
                        "url": article.url,
                    }
                    articles_list.append(article_info)
                    article_processed = (
                        True  # Set the flag to True for successful processing
                    )
                    break  # Successful parsing, exit retry loop

            except Exception as e:
                print(f"Error processing article (Retry {retries + 1}):", e)
                retries += 1
                if retries >= max_retries:
                    article_processed = (
                        False  # Set the flag to back False for unsuccessful processing
                    )
                    print(f"Maximum retries ({max_retries}) reached for this article.")
                    break  # Maximum retries reached, exit retry loop
        if not article_processed:
            # Break out of the outer for loop if the article couldn't be processed after max_retries.
            print("Skipping article due to processing errors.")
            break

    return articles_list


if __name__ == "__main__":
    articles = get_recent_articles(dailypost_url, max_age_days=4)
    for idx, article in enumerate(articles, start=1):
        print(f"Article {idx}:")
        print(f"Title: {article['title']}")
        print(f"Text: {article['text']}")
        print(f"URL: {article['url']}")
        print("\n")
