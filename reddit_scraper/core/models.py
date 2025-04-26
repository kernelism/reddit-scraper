from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Model representing a Reddit comment."""

    body: str
    user: str
    time: datetime
    replies: List["Comment"] = Field(default_factory=list)


class Post(BaseModel):
    """Model representing a Reddit post."""

    post_body: str
    post_user: str
    post_time: datetime
    comments: List[Comment] = Field(default_factory=list)


class SubredditConfig(BaseModel):
    """Model for subreddit configuration."""

    name: str
    url: str


class ScraperState(BaseModel):
    """Model for scraper checkpoint state."""

    processed_ids: List[str] = Field(default_factory=list)
    remaining_ids: List[str] = Field(default_factory=list)


class ScraperConfig(BaseModel):
    """Model for scraper configuration."""

    chrome_options: List[str]
    driver_path_env: str
    base_url: str
    checkpoint_file: str
    data_dir: str
    post_link_attr: dict
