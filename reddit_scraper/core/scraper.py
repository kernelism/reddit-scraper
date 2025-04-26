import json
import os
import time
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from reddit_scraper.core.data_processor import DataProcessor
from reddit_scraper.core.models import Comment, Post, ScraperState
from reddit_scraper.utils.config import get_scraper_config


class RedditScraper:
    """A class to handle Reddit scraping operations."""

    def __init__(self, subreddit: str, post_limit: int = None) -> None:
        """Initialize the scraper with a subreddit."""
        self.config = get_scraper_config()
        self.subreddit = subreddit
        self.post_limit = post_limit
        self.driver = self._setup_driver()
        self.post_ids: List[str] = []
        self.processed_ids: List[str] = []
        self.posts: List[Post] = []
        self.checkpointed: bool = False
        self.data_processor = DataProcessor()

    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and return a configured Chrome WebDriver."""
        options = Options()
        for arg in self.config.chrome_options:
            options.add_argument(arg)
        return webdriver.Chrome(
            service=Service(os.getenv(self.config.driver_path_env)), options=options
        )

    def lazy_scroll(self) -> str:
        """Scroll the page lazily to load all content."""
        current_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == current_height:
                break
            current_height = new_height
        return self.driver.page_source

    def get_posts(self) -> None:
        """Get all posts from the subreddit."""
        self.driver.get(self.subreddit)
        self.driver.maximize_window()
        time.sleep(5)
        html = self.lazy_scroll()
        parser = BeautifulSoup(html, "html.parser")
        post_links = parser.find_all("a", self.config.post_link_attr)
        print(f"Found {len(post_links)} posts for subreddit {self.subreddit}")

        for post_link in post_links:
            post_id = post_link["href"].split("/")[-3]
            if post_id not in self.post_ids:
                self.post_ids.append(post_id)

            # Stop if we've reached the post limit
            if self.post_limit and len(self.post_ids) >= self.post_limit:
                print(f"Reached post limit of {self.post_limit}")
                break

    def save_state(self) -> None:
        """Save the current scraping state."""
        state = ScraperState(
            processed_ids=self.processed_ids,
            remaining_ids=[x for x in self.post_ids if x not in self.processed_ids],
        )
        with open(self.config.checkpoint_file, "w") as file:
            json.dump(state.dict(), file)

    def load_state(self) -> None:
        """Load the previous scraping state."""
        try:
            with open(self.config.checkpoint_file, "r") as file:
                state = ScraperState(**json.load(file))
                self.processed_ids = state.processed_ids
                self.post_ids = state.remaining_ids
        except FileNotFoundError:
            self.processed_ids = []

    def get_data(self, post_id: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific post."""
        url = f"{self.config.base_url}{post_id}.json"
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        text = soup.find("body").get_text()

        if "Too Many Requests" in text:
            return None

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print(f"Error parsing JSON for post {post_id}")
            return None

    def get_post_details(self) -> bool:
        """Get details for all posts."""
        if self.checkpointed:
            self.load_state()
            self.restart()
            self.checkpointed = False
            print("Resuming from checkpoint...")

        for post_id in self.post_ids:
            if post_id in self.processed_ids:
                continue

            print(f"Getting data for post {post_id}")
            json_data = self.get_data(post_id)

            if json_data is None:
                self.save_state()
                self.destroy()
                self.checkpointed = True
                print("Error 429 encountered. Session stopped.")
                return self.checkpointed

            try:
                post = self.data_processor.parse_post_data(json_data)
                self.posts.append(post)
                self.processed_ids.append(post_id)
            except Exception as e:
                print(f"Error processing post {post_id}: {e}")
                continue

        return self.checkpointed

    def restart(self) -> None:
        """Restart the WebDriver."""
        self.driver = self._setup_driver()

    def destroy(self) -> None:
        """Clean up resources."""
        self.driver.quit()
