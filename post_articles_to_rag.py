import json
import time

import requests

# Path to your JSON file
JSON_FILE = "./news_articles.json"

# API endpoint
API_URL = "http://localhost:5000/documents"


def post_articles(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Found {len(articles)} articles to post.")

    for idx, article in enumerate(articles, start=1):
        try:
            response = requests.post(API_URL, json=article)
            if response.status_code == 200 or response.status_code == 201:
                print(f"✅ Posted ({idx}/{len(articles)}): {article.get('title')}")
            else:
                print(f"❌ Failed ({idx}/{len(articles)}): {article.get('title')} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error posting ({idx}/{len(articles)}): {article.get('title')} - {e}")

        # Wait 1 second before next post
        time.sleep(1)


if __name__ == "__main__":
    post_articles(JSON_FILE)
