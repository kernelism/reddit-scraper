"""Shared test fixtures."""
import os
from pathlib import Path

import pytest


@pytest.fixture
def sample_subreddits_json(tmp_path):
    """Create a sample subreddits.json file."""
    subreddits = ["programming", "python", "physics", "biology"]
    json_file = tmp_path / "subreddits.json"
    with open(json_file, "w") as f:
        import json

        json.dump(subreddits, f)
    return json_file


@pytest.fixture
def sample_post_data():
    """Create sample post data for testing."""
    import json
    from datetime import datetime

    now = int(datetime.now().timestamp())

    return [
        {
            "data": {
                "children": [
                    {
                        "data": {
                            "title": "Test Post",
                            "author": "testuser",
                            "created_utc": now,
                        }
                    }
                ]
            }
        },
        {
            "data": {
                "children": [
                    {
                        "kind": "t1",
                        "data": {
                            "body": "Test Comment",
                            "author": "testuser",
                            "created_utc": now,
                            "replies": {"data": {"children": []}},
                        },
                    }
                ]
            }
        },
    ]
