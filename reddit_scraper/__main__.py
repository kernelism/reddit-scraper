"""Reddit Scraper - A simple tool to scrape posts and comments from Reddit subreddits."""

import click
from dotenv import load_dotenv

from reddit_scraper.core.data_processor import DataProcessor
from reddit_scraper.core.models import SubredditConfig
from reddit_scraper.core.scraper import RedditScraper

load_dotenv()


def process_subreddit(
    subreddit_config: SubredditConfig, post_limit: int = None
) -> None:
    """Process a single subreddit."""
    print(f"Scraping subreddit: {subreddit_config.name}")
    scraper = RedditScraper(subreddit=subreddit_config.url, post_limit=post_limit)
    processor = DataProcessor()

    try:
        scraper.get_posts()
        while True:
            checkpointed = scraper.get_post_details()
            if not checkpointed:
                break

        processor.save_to_json(scraper.posts, subreddit_config.name)
    except Exception as e:
        print(f"Error processing subreddit {subreddit_config.name}: {e}")
    finally:
        scraper.destroy()


@click.command()
@click.option(
    "-d",
    "--duration",
    prompt="Scrape Duration",
    help="Duration to scrape for (month/year)",
)
@click.option(
    "-s",
    "--subreddits-file",
    default="subreddits.json",
    help="Path to the subreddits JSON file",
)
@click.option(
    "-l",
    "--post-limit",
    type=int,
    help="Maximum number of posts to scrape per subreddit",
)
def main(duration: str, subreddits_file: str, post_limit: int = None) -> None:
    """Main entry point for the Reddit scraper."""
    if duration not in ["month", "year"]:
        raise ValueError("Duration must be either month or year")

    processor = DataProcessor()
    subreddits = processor.read_subreddits_from_json(subreddits_file, duration)

    for subreddit_config in subreddits:
        process_subreddit(subreddit_config, post_limit)


if __name__ == "__main__":
    main()
