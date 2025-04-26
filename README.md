# Reddit Scraper

A simple tool to scrape posts and comments from Reddit subreddits.

## What it does

- Scrapes top posts and their comments from specified subreddits
- Supports monthly or yearly time periods
- Can limit the number of posts scraped per subreddit
- Saves data in JSON format for easy analysis

## How it works

### The Smart Way to Scrape Reddit

Instead of brute-forcing our way through Reddit's pages, we use a clever approach that's both efficient and respectful of Reddit's servers:

First, we visit the subreddit's top posts page and scroll through it just like a human would. As we scroll, we collect the IDs of all the posts we want to save. This is quick and lightweight - we're just gathering a list of what we want to look at later.

Then, for each post we're interested in, we use Reddit's own API to get all the data in a clean, structured format. We do this by adding `.json` to the end of any Reddit URL, which gives us everything we need in one go - the post itself, all its comments, and all the metadata.

This approach has several advantages:
- It's much faster than downloading and parsing entire HTML pages
- We get clean, structured data instead of messy HTML
- We can easily resume if something goes wrong
- We're less likely to trigger Reddit's rate limits

### Handling Reddit's Limits

Reddit doesn't like it when people make too many requests too quickly. Our scraper is smart about this:

- If Reddit tells us we're asking for too much too quickly, we save our progress and wait
- We can pick up right where we left off when we run the scraper again
- We add small delays between requests to be nice to Reddit's servers

This makes our scraper more reliable and less likely to get blocked.

## Installation

### From source

```bash
git clone https://github.com/yourusername/reddit-scraper.git
cd reddit-scraper
pip install -e .
```

### Using pip

```bash
pip install reddit-scraper
```

## Usage

1. Create a `subreddits.json` file with your target subreddits:

```json
[
    "programming",
    "python",
    "physics",
    "biology"
]
```

2. Run the scraper:

```bash
reddit-scraper -d month -s subreddits.json
```

3. To limit posts per subreddit:

```bash
reddit-scraper -d month -s subreddits.json -l 50
```

## Options

- `-d, --duration`: Time period (month/year)
- `-l, --post-limit`: Max posts per subreddit
- `-s, --subreddits-file`: Path to subreddits config file

## Output

Data is saved in JSON files under the `data/` directory, one file per subreddit.

### Output Format

The scraper generates JSON files with a clean, structured format that's easy to work with. Here's what the output looks like:

```json
[
  {
    "post_body": "This is the title of the post",
    "post_user": "username123",
    "post_time": "2023-04-15T14:30:45",
    "comments": [
      {
        "body": "This is a top-level comment",
        "user": "commenter456",
        "time": "2023-04-15T15:20:10",
        "replies": [
          {
            "body": "This is a reply to the comment",
            "user": "replier789",
            "time": "2023-04-15T16:05:30",
            "replies": []
          }
        ]
      }
    ]
  },
  {
    "post_body": "Another post title",
    "post_user": "anotheruser",
    "post_time": "2023-04-14T09:15:22",
    "comments": []
  }
]
```

Key features of the output format:

- **Posts**: Each post is represented as an object with:
  - `post_body`: The title of the post
  - `post_user`: The username of the post author
  - `post_time`: ISO-formatted timestamp of when the post was created
  - `comments`: Array of comments on the post

- **Comments**: Each comment is represented as an object with:
  - `body`: The text content of the comment
  - `user`: The username of the comment author
  - `time`: ISO-formatted timestamp of when the comment was created
  - `replies`: Array of replies to the comment (nested comments)

- **Nested Structure**: Comments can have replies, which can have their own replies, creating a tree structure that preserves the conversation flow

This format makes it easy to:
- Analyze post and comment content
- Track user activity
- Measure engagement over time
- Import into data analysis tools

## Development

### Project Structure

```
reddit-scraper/
├── reddit_scraper/           # Main package
│   ├── core/                 # Core functionality
│   │   ├── models.py         # Data models
│   │   ├── scraper.py        # Scraping logic
│   │   └── data_processor.py # Data processing
│   ├── utils/                # Utilities
│   │   └── config.py         # Configuration
│   ├── __init__.py           # Package initialization
│   └── __main__.py           # Entry point
├── tests/                    # Test suite
├── setup.py                  # Package setup
├── requirements.txt          # Dependencies
└── README.md                 # Documentation
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To set them up:

```bash
pre-commit install
```

The hooks will run automatically on commit, or you can run them manually:

```bash
pre-commit run --all-files
```

### Testing

Run the tests with:

```bash
pytest
```

For coverage information:

```bash
pytest --cov=. --cov-report=term-missing
```
