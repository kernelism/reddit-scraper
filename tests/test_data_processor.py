"""Tests for the data_processor module."""
import json
import os
from datetime import datetime
from unittest.mock import patch

import pytest

from reddit_scraper.core.data_processor import DataProcessor, DateTimeEncoder
from reddit_scraper.core.models import Comment, Post


def test_datetime_encoder():
    """Test the DateTimeEncoder class."""
    now = datetime.now()
    encoded = json.dumps({"time": now}, cls=DateTimeEncoder)
    decoded = json.loads(encoded)

    assert decoded["time"] == now.isoformat()


@patch("reddit_scraper.core.data_processor.get_scraper_config")
def test_save_to_json(mock_get_config, tmp_path):
    """Test saving data to JSON."""
    # Setup mock config
    mock_config = mock_get_config.return_value
    mock_config.data_dir = str(tmp_path)

    # Create test data
    now = datetime.now()
    comment = Comment(body="Test comment", user="testuser", time=now, replies=[])

    post = Post(
        post_body="Test post", post_user="testuser", post_time=now, comments=[comment]
    )

    # Save data
    processor = DataProcessor()
    filename = processor.save_to_json([post], "testsubreddit")

    # Check file was created
    assert os.path.exists(filename)
    assert filename.endswith("testsubreddit.json")

    # Check file contents
    with open(filename, "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["post_body"] == "Test post"
    assert data[0]["post_user"] == "testuser"
    assert data[0]["post_time"] == now.isoformat()
    assert len(data[0]["comments"]) == 1
    assert data[0]["comments"][0]["body"] == "Test comment"


@patch("reddit_scraper.core.data_processor.get_scraper_config")
def test_read_subreddits_from_json(mock_get_config, tmp_path):
    """Test reading subreddits from JSON."""
    # Setup mock config
    mock_config = mock_get_config.return_value

    # Create test JSON file
    subreddits = ["subreddit1", "subreddit2"]
    json_file = tmp_path / "subreddits.json"
    with open(json_file, "w") as f:
        json.dump(subreddits, f)

    # Read subreddits
    processor = DataProcessor()
    configs = processor.read_subreddits_from_json(str(json_file), "month")

    # Check results
    assert len(configs) == 2
    assert configs[0].name == "subreddit1"
    assert configs[0].url == "https://www.reddit.com/r/subreddit1/top/?t=month"
    assert configs[1].name == "subreddit2"
    assert configs[1].url == "https://www.reddit.com/r/subreddit2/top/?t=month"
