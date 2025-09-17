# News Source Scraper

This module provides tools for scraping news articles from The Guardian and posting them to a RAG (Retrieval-Augmented Generation) chatbot backend.

## Overview

The news source module consists of two main components:

1. **`reuters_scraper.py`** - Scrapes news articles from The Guardian's sitemap
2. **`post_articles_to_rag.py`** - Posts scraped articles to the RAG backend API

## Features

- Scrapes articles from The Guardian using their news sitemap
- Extracts structured article data including title, content, metadata
- Saves articles to JSON format for processing
- Posts articles to RAG backend with rate limiting
- Handles errors gracefully with detailed logging

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Scraping Articles

Run the scraper to fetch articles from The Guardian:

```bash
python reuters_scraper.py
```

This will:

- Fetch The Guardian's news sitemap
- Extract article URLs
- Scrape up to 70 articles (configurable)
- Save results to `news_articles.json`

### Posting Articles to RAG Backend

After scraping, post the articles to your RAG backend:

```bash
python post_articles_to_rag.py
```

This will:

- Read articles from `news_articles.json`
- Post each article to `http://localhost:5000/documents`
- Include rate limiting (1 second between requests)
- Display progress and error information

## Configuration

### Scraper Settings

In `reuters_scraper.py`, you can modify:

- `SITEMAP_URL`: Change the news source (currently The Guardian)
- `limit` parameter in `scrape_articles()`: Adjust number of articles to scrape

### API Settings

In `post_articles_to_rag.py`, you can modify:

- `API_URL`: Change the backend endpoint URL
- Rate limiting delay in the `time.sleep()` call

## File Structure

```
news-source/
├── reuters_scraper.py      # Main scraper script
├── post_articles_to_rag.py # API posting script
├── news_articles.json      # Generated article data
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Article Data Structure

Each scraped article follows this JSON structure:

```json
{
  "id": "unique-uuid",
  "title": "Article Title",
  "content": "Full article text content",
  "metadata": {
    "authors": ["Author Name"],
    "date_publish": "2024-01-01T00:00:00",
    "description": "Article description",
    "url": "https://source-url.com/article",
    "source_domain": "theguardian.com"
  }
}
```

## Error Handling

Both scripts include comprehensive error handling:

- Network timeouts and connection errors
- Invalid article content (empty or malformed)
- API posting failures with status codes
- Graceful skipping of problematic URLs

## Dependencies

- **requests**: HTTP library for API calls and web scraping
- **newsplease**: News article extraction library
- **xml.etree.ElementTree**: XML parsing for sitemaps (built-in)
- **json**: JSON handling (built-in)
- **uuid**: Unique identifier generation (built-in)

## Notes

- The scraper currently targets The Guardian but can be adapted for other news sources
- Rate limiting is implemented to be respectful to both the news source and RAG backend
- Articles are filtered to exclude non-HTML content (images, PDFs, etc.)
- The system requires the RAG backend to be running on `localhost:5000`
