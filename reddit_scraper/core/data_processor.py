import json
import os
from datetime import datetime
from typing import Any, Dict, List

from reddit_scraper.core.models import Comment, Post, SubredditConfig
from reddit_scraper.utils.config import get_scraper_config


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class DataProcessor:
    """Handles data processing and storage operations."""

    def __init__(self):
        """Initialize the data processor."""
        self.config = get_scraper_config()

    def parse_post_data(self, json_data: Dict[str, Any]) -> Post:
        """Parse raw JSON data into a Post model."""
        post = json_data[0]["data"]["children"][0]["data"]
        comments_data = json_data[1]["data"]["children"]

        return Post(
            post_body=post["title"],
            post_user=post["author"],
            post_time=datetime.fromtimestamp(post["created_utc"]),
            comments=self._parse_comments(comments_data),
        )

    def _parse_comments(self, comment_data: List[Dict[str, Any]]) -> List[Comment]:
        """Parse comment data into Comment models."""
        comments = []
        for comment in comment_data:
            if comment["kind"] != "t1":
                continue

            comment_dict = comment["data"]
            comments.append(
                Comment(
                    body=comment_dict["body"],
                    user=comment_dict["author"],
                    time=datetime.fromtimestamp(comment_dict["created_utc"]),
                    replies=self._parse_comments(
                        comment_dict["replies"]["data"]["children"]
                    )
                    if comment_dict.get("replies")
                    else [],
                )
            )
        return comments

    def save_to_json(self, data: List[Post], subreddit: str) -> str:
        """Save processed data to a JSON file."""
        directory = self.config.data_dir
        os.makedirs(directory, exist_ok=True)
        filename = f"{directory}/{subreddit}.json"

        with open(filename, "w") as f:
            json.dump([post.dict() for post in data], f, cls=DateTimeEncoder)
        return filename

    def read_subreddits_from_json(
        self, filename: str, duration: str
    ) -> List[SubredditConfig]:
        """Read subreddit configurations from a JSON file."""
        with open(filename) as f:
            subreddits_list = json.load(f)

        return [
            SubredditConfig(
                name=subreddit,
                url=f"https://www.reddit.com/r/{subreddit}/top/?t={duration}",
            )
            for subreddit in subreddits_list
        ]
