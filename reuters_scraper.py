import json
import uuid
import xml.etree.ElementTree as ET

import requests
from newsplease import NewsPlease

# BBC News sitemap
SITEMAP_URL = "https://www.theguardian.com/sitemaps/news.xml"


def fetch_sitemap(url):
    """Fetch and parse XML sitemap."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return ET.fromstring(resp.content)


def extract_article_links(sitemap_xml):
    """Extract all article URLs from sitemap XML."""
    return [elem.text for elem in sitemap_xml.findall(".//{*}loc")]


def scrape_articles(urls, limit=70):
    """Scrape articles using news-please and return structured documents."""
    documents = []
    count = 0

    for url in urls:
        if count >= limit:
            break

        # Skip non-HTML URLs
        if any(ext in url for ext in [".jpg", ".png", ".pdf", ".gif"]):
            continue

        try:
            article = NewsPlease.from_url(url)
            if article and article.maintext:
                doc = {
                    "id": str(uuid.uuid4()),
                    "title": article.title or "",
                    "content": article.maintext,
                    "metadata": {
                        "authors": article.authors,
                        "date_publish": str(article.date_publish) if article.date_publish else None,
                        "description": article.description,
                        "url": url,
                        "source_domain": article.source_domain,
                    },
                }
                documents.append(doc)
                count += 1
                print(f"✅ Scraped ({count}/{limit}): {article.title}")
            else:
                print(f"⚠️ Skipped (empty content): {url}")
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")

    return documents


def save_json(documents, filename="news_articles.json"):
    """Save the documents list to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)
    print(f"\n📂 Saved {len(documents)} articles to {filename}")


if __name__ == "__main__":
    print("🔎 Fetching theguardian sitemap...")
    root = fetch_sitemap(SITEMAP_URL)

    article_urls = extract_article_links(root)
    print(f"Found {len(article_urls)} article URLs")

    # Scrape first 50 articles
    documents = scrape_articles(article_urls)

    save_json(documents)
