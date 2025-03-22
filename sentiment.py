from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from scraping import get_news_articles  # Import the scraping function
from comparative_analysis import comparative_analysis  
from comparative_analysis import extract_topics  # Import the extract_topics function

# Load model and tokenizer once globally
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Set up sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Label mapping from model index or label to human-readable label
LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive",
    "NEGATIVE": "Negative",
    "NEUTRAL": "Neutral",
    "POSITIVE": "Positive"
}

def analyze_sentiment(text):
    """
    Performs sentiment analysis on the input text using a transformer model.

    Args:
        text (str): The article content or summary.

    Returns:
        dict: Sentiment label and score
    """
    try:
        result = sentiment_pipeline(text[:512])[0]  # Limit to 512 tokens
        raw_label = result['label'].strip().upper()
        score = round(result['score'], 3)

        # Try to get mapped label first
        sentiment = LABEL_MAP.get(raw_label)

        # Fallback score-based sentiment classification
        if not sentiment:
            if score >= 0.6:
                sentiment = "Positive"
            elif score <= 0.4:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "score": score
        }

    except Exception as e:
        print(f"[ERROR] Sentiment analysis failed: {e}")
        return {
            "sentiment": "Neutral",
            "score": 0.5
        }

def analyze_articles(articles):
    """
    Adds sentiment analysis to each article.

    Args:
        articles (list): List of articles with summaries.

    Returns:
        list: Articles with added sentiment analysis.
    """
    for article in articles:
        try:
            # Use full text if available, otherwise use the summary
            text_to_analyze = article.get("summary", "").strip()
            if not text_to_analyze:
                print(f"[WARN] Skipping article with missing or empty summary: {article.get('title', 'Untitled')}")
                article["Sentiment"] = "Unknown"
                article["Sentiment Score"] = 0.0
                continue

            sentiment_result = analyze_sentiment(text_to_analyze)
            article["Sentiment"] = sentiment_result["sentiment"]
            article["Sentiment Score"] = sentiment_result["score"]
        except Exception as e:
            print(f"[WARN] Sentiment analysis failed for article: {article.get('title', 'Untitled')}. Error: {e}")
            article["Sentiment"] = "Unknown"
            article["Sentiment Score"] = 0.0

    return articles

def get_news_articles_with_sentiment(company_name: str, limit: int = 10) -> dict:
    """
    Fetches news articles, performs sentiment analysis, and extracts topics.
    """
    # Fetch articles from the scraping module
    fetched_data = get_news_articles(company_name, limit=limit)

    # Extract the list of articles
    articles = fetched_data.get("Articles", [])
    if not articles:
        print(f"[WARN] No articles found for {company_name}.")
        return {"Articles": []}

    print(f"[INFO] Number of articles fetched: {len(articles)}")

    enriched_articles = []

    for article in articles:
        # Ensure article is a dictionary
        if not isinstance(article, dict):
            print(f"[WARN] Skipping invalid article: {article}")
            continue

        # Perform sentiment analysis
        text_to_analyze = article.get("summary", "").strip()
        if not text_to_analyze:
            print(f"[WARN] Skipping article with missing or empty summary: {article.get('title', 'Untitled')}")
            continue

        sentiment_data = analyze_sentiment(text_to_analyze)
        sentiment = sentiment_data["sentiment"]
        sentiment_score = sentiment_data["score"]

        # Extract topics
        topics = extract_topics(text_to_analyze) if text_to_analyze else []

        # Enrich the article with sentiment and topics
        enriched_article = {
            "Title": article.get("title", "Untitled"),
            "Summary": text_to_analyze,
            "Sentiment": sentiment,
            "Sentiment Score": sentiment_score,
            "Topics": topics,
            "Publish Date": article.get("publish_date", "N/A"),
            "URL": article.get("url", "N/A")
        }
        enriched_articles.append(enriched_article)

        # Debugging: Print the enriched article
        print("DEBUG: Enriched article:", enriched_article)

    return {"Articles": enriched_articles}

if __name__ == "__main__":
    company = "Tesla"
    news_data = get_news_articles_with_sentiment(company)

    if not news_data["Articles"]:
        print(f"No articles found for {company}.")
    else:
        import json
        print(json.dumps(news_data, indent=4))