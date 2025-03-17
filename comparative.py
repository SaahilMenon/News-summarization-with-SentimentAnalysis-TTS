from collections import Counter
from sentiment.py import analyze_sentiment

def comparative_analysis(articles):
    sentiment_counts = Counter()
    sentiment_results = []

    for article in articles:
        sentiment = analyze_sentiment(article['title'])
        sentiment_counts[sentiment] += 1
        sentiment_results.append({"title": article['title'], "sentiment": sentiment})

    return {
        "sentiment_distribution": dict(sentiment_counts),
        "articles_analysis": sentiment_results
    }
