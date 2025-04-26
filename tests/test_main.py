"""Tests for the main module."""
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from reddit_scraper.__main__ import main, process_subreddit
from reddit_scraper.core.models import SubredditConfig


@patch("reddit_scraper.__main__.RedditScraper")
@patch("reddit_scraper.__main__.DataProcessor")
def test_process_subreddit(mock_data_processor, mock_reddit_scraper):
    """Test processing a subreddit."""
    # Setup mocks
    mock_scraper_instance = mock_reddit_scraper.return_value
    mock_scraper_instance.get_post_details.return_value = False
    mock_scraper_instance.posts = []

    # Create test config
    config = SubredditConfig(
        name="testsubreddit", url="https://www.reddit.com/r/testsubreddit/"
    )

    # Process subreddit
    process_subreddit(config, post_limit=10)

    # Check mocks were called correctly
    mock_reddit_scraper.assert_called_once_with(
        subreddit="https://www.reddit.com/r/testsubreddit/", post_limit=10
    )
    mock_scraper_instance.get_posts.assert_called_once()
    mock_scraper_instance.get_post_details.assert_called_once()
    mock_scraper_instance.destroy.assert_called_once()


@patch("reddit_scraper.__main__.process_subreddit")
@patch("reddit_scraper.__main__.DataProcessor")
def test_main(mock_data_processor, mock_process_subreddit):
    """Test the main function."""
    # Setup mocks
    mock_processor_instance = mock_data_processor.return_value
    mock_processor_instance.read_subreddits_from_json.return_value = [
        SubredditConfig(name="subreddit1", url="https://www.reddit.com/r/subreddit1/"),
        SubredditConfig(name="subreddit2", url="https://www.reddit.com/r/subreddit2/"),
    ]

    # Create Click test runner
    runner = CliRunner()

    # Run main function with Click test runner
    result = runner.invoke(
        main,
        [
            "--duration",
            "month",
            "--subreddits-file",
            "subreddits.json",
            "--post-limit",
            "20",
        ],
    )

    # Check that the command executed successfully
    assert result.exit_code == 0

    # Check mocks were called correctly
    mock_processor_instance.read_subreddits_from_json.assert_called_once_with(
        "subreddits.json", "month"
    )

    # Check that process_subreddit was called twice (once for each subreddit)
    assert mock_process_subreddit.call_count == 2

    # Get the actual calls made to process_subreddit
    calls = mock_process_subreddit.call_args_list

    # Check first call
    first_call = calls[0]
    first_config = first_call[0][0]  # First positional argument
    first_post_limit = first_call[0][1]  # Second positional argument

    assert first_config.name == "subreddit1"
    assert first_config.url == "https://www.reddit.com/r/subreddit1/"
    assert first_post_limit == 20

    # Check second call
    second_call = calls[1]
    second_config = second_call[0][0]  # First positional argument
    second_post_limit = second_call[0][1]  # Second positional argument

    assert second_config.name == "subreddit2"
    assert second_config.url == "https://www.reddit.com/r/subreddit2/"
    assert second_post_limit == 20
