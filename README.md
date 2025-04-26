# Reddit Scraper

A simple tool to scrape posts and comments from Reddit subreddits.

## What it does

- Scrapes top posts and their comments from specified subreddits
- Supports monthly or yearly time periods
- Can limit the number of posts scraped per subreddit
- Saves data in JSON format for easy analysis

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
