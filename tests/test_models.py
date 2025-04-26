"""Tests for the models module."""
from datetime import datetime

import pytest

from reddit_scraper.core.models import Comment, Post, SubredditConfig


def test_comment_creation():
    """Test creating a Comment object."""
    now = datetime.now()
    comment = Comment(body="Test comment", user="testuser", time=now, replies=[])

    assert comment.body == "Test comment"
    assert comment.user == "testuser"
    assert comment.time == now
    assert comment.replies == []


def test_post_creation():
    """Test creating a Post object."""
    now = datetime.now()
    comment = Comment(body="Test comment", user="testuser", time=now, replies=[])

    post = Post(
        post_body="Test post", post_user="testuser", post_time=now, comments=[comment]
    )

    assert post.post_body == "Test post"
    assert post.post_user == "testuser"
    assert post.post_time == now
    assert len(post.comments) == 1
    assert post.comments[0].body == "Test comment"


def test_subreddit_config_creation():
    """Test creating a SubredditConfig object."""
    config = SubredditConfig(
        name="testsubreddit", url="https://www.reddit.com/r/testsubreddit/"
    )

    assert config.name == "testsubreddit"
    assert config.url == "https://www.reddit.com/r/testsubreddit/"
