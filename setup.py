from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="reddit-scraper",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple tool to scrape posts and comments from Reddit subreddits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/reddit-scraper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "reddit-scraper=reddit_scraper.__main__:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "pytest-xdist>=3.3.1",
            "black>=23.3.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "flake8-docstrings>=1.7.0",
            "pre-commit>=3.3.3",
        ],
    },
)
