from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from scraping import get_news_articles  # Import the scraping function
from comparative_analysis import comparative_analysis  

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
            "sentiment": "Unknown",
            "score": 0.0
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
            text_to_analyze = article.get("Text", article["Summary"])
            sentiment_result = analyze_sentiment(text_to_analyze)
            article["Sentiment"] = sentiment_result["sentiment"]
            article["Sentiment Score"] = sentiment_result["score"]
        except Exception as e:
            print(f"[WARN] Sentiment analysis failed for article: {article['Title']}. Error: {e}")
            article["Sentiment"] = "Unknown"
            article["Sentiment Score"] = 0.0

    return articles

def get_news_articles_with_sentiment(company_name, limit=10):
    """
    Fetches news articles, adds sentiment analysis, and performs comparative analysis.

    Args:
        company_name (str): The name of the company to fetch news for.
        limit (int): The maximum number of articles to fetch.

    Returns:
        dict: News data with sentiment and comparative analysis.
    """
    news_data = get_news_articles(company_name, limit)  # Fetch articles from scraping.py
    articles = news_data["Articles"]

    if articles:
        articles = analyze_articles(articles)  # Add sentiment analysis
        news_data["Articles"] = articles

        
        comparative_data = comparative_analysis(articles)
        news_data["Comparative Sentiment Score"] = comparative_data

    return news_data

if __name__ == "__main__":
    company = "Tesla"
    news_data = get_news_articles_with_sentiment(company)

    if not news_data["Articles"]:
        print(f"No articles found for {company}.")
    else:
        import json
        print(json.dumps(news_data, indent=4)) 