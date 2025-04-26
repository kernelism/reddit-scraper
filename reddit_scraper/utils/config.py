import os
from typing import Any, Dict

from pydantic_settings import BaseSettings

from reddit_scraper.core.models import ScraperConfig


class Settings(BaseSettings):
    """Application settings."""

    CHROME_OPTIONS: list = ["--no-sandbox", "--disable-dev-shm-usage"]
    DRIVER_PATH_ENV: str = "DRIVER_PATH"
    BASE_URL: str = "https://reddit.com/"
    POST_LINK_ATTR: dict = {"slot": "full-post-link"}
    CHECKPOINT_FILE: str = "checkpoint.json"
    DATA_DIR: str = "data"

    class Config:
        env_prefix = "REDDIT_SCRAPER_"


def get_scraper_config() -> ScraperConfig:
    """Get scraper configuration."""
    settings = Settings()
    return ScraperConfig(
        chrome_options=settings.CHROME_OPTIONS,
        driver_path_env=settings.DRIVER_PATH_ENV,
        base_url=settings.BASE_URL,
        checkpoint_file=settings.CHECKPOINT_FILE,
        data_dir=settings.DATA_DIR,
        post_link_attr=settings.POST_LINK_ATTR,
    )
