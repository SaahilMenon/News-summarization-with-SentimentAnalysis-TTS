import requests
from bs4 import BeautifulSoup
import re
import random
from urllib.parse import urlparse

# User-Agent rotation for better request handling
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (X11; Linux x86_64)'
]

def fetch_bing_news(company_name, limit=10):
    """
    Fetches news articles from Bing News search results for a given company.

    Args:
        company_name (str): The company or topic name to search for.
        limit (int): The maximum number of articles to fetch.

    Returns:
        list: A list of dictionaries containing article details (title, summary, source_and_time, url).
    """
    base_url = "https://www.bing.com/news/search?q="
    query = f"{company_name} news"
    url = f"{base_url}{query.replace(' ', '+')}"

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch Bing News: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    seen_urls = set()  # To ensure unique articles

    # Find news articles in the search results
    for result in soup.find_all("div", class_="news-card newsitem cardcommon"):  # Updated class name
        try:
            # Extract title
            title = result.get("data-title", "No title available")

            # Extract link
            link = result.get("data-url", None)

            # Skip articles with missing title or URL
            if not title or not link:
                print(f"[WARN] Skipping article due to missing title or URL.")
                continue

            # Extract snippet (if available)
            snippet_tag = result.find("div", class_="snippet")
            snippet = snippet_tag.text.strip() if snippet_tag else "No summary available"

            # Extract source and time (if available)
            source_tag = result.find("div", class_="source")
            source_and_time = source_tag.text.strip() if source_tag else "Unknown source"

            # Normalize the URL to avoid duplicates
            normalized_link = urlparse(link).netloc + urlparse(link).path if link else None
            if normalized_link in seen_urls:
                continue

            articles.append({
                "title": title,  # Standardized key
                "summary": snippet,  # Standardized key
                "source_and_time": source_and_time,  # Standardized key
                "url": link  # Standardized key
            })
            seen_urls.add(normalized_link)

            # Debug: Print the fetched article
            print(f"[DEBUG] Article fetched: {articles[-1]}")

            # Stop if the required number of articles is reached
            if len(articles) >= limit:
                break
        except Exception as e:
            print(f"[WARN] Skipping a result due to error: {e}. Result: {result}")
            continue

    # Debug: Print the number of articles fetched
    print(f"[INFO] Number of articles fetched: {len(articles)}")
    return articles

def get_news_articles(company_name, limit=10):
    """
    Fetches and processes news articles: extracting content, summarizing, and displaying metadata.
    """
    articles = fetch_bing_news(company_name, limit)
    return {
        "Company": company_name,
        "Articles": articles
    }

