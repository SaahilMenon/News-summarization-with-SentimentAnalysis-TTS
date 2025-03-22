from collections import Counter
import statistics
import re

def extract_topics(text: str, top_n: int = 3) -> list:
    """
    Extract key topics from article titles or summaries using simple NLP logic.
    """
    if not text or not isinstance(text, str):
        return []
    # Extract words with at least 4 characters and filter out stopwords
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {
        "about", "from", "with", "this", "that", "which", "have", "been", "they",
        "will", "their", "into", "more", "news"
    }
    filtered = [w for w in words if w not in stopwords]
    return list(dict(Counter(filtered).most_common(top_n)).keys())

def find_common_topics(unique_topics):
    """
    Finds the most common topic across all articles.
    """
    all_topics = []
    for topics in unique_topics.values():
        all_topics.extend(topics)

    common_topic = None
    topic_counts = Counter(all_topics)
    if topic_counts:
        common_topic = topic_counts.most_common(1)[0][0]  # Get the most frequent topic

    return common_topic

def determine_final_sentiment(sentiment_distribution, avg_score):
    """
    Determines the final sentiment analysis based on sentiment distribution and average score.
    """
    positive_count = sentiment_distribution.get("Positive", 0)
    negative_count = sentiment_distribution.get("Negative", 0)

    if positive_count > negative_count and avg_score > 0.6:
        return "Overall sentiment is mostly positive."
    elif negative_count > positive_count and avg_score < 0.4:
        return "Overall sentiment is mostly negative."
    else:
        return "Overall sentiment is neutral."

def comparative_analysis(articles):
    """
    Performs comparative analysis on the given articles.

    Args:
        articles (list): List of articles with sentiment data.

    Returns:
        dict: Comparative sentiment analysis results.
    """
    # Calculate sentiment distribution
    sentiment_distribution = Counter(article["Sentiment"] for article in articles)

    # Calculate average sentiment score
    scores = [article.get("Sentiment Score", 0.0) for article in articles if isinstance(article.get("Sentiment Score", 0.0), (int, float))]
    avg_score = round(statistics.mean(scores), 3) if scores else 0.0

    # Generate coverage differences
    coverage_differences = []
    for i, article1 in enumerate(articles):
        for j, article2 in enumerate(articles):
            if i >= j:
                continue
            comparison = {
                "Comparison": f"Article {i+1} vs Article {j+1}",
                "Impact": f"Article {i+1} discusses {article1['Summary'][:50]}... while Article {j+1} focuses on {article2['Summary'][:50]}..."
            }
            coverage_differences.append(comparison)

    # Extract topics and calculate topic overlap
    topic_overlap = {"Common Topics": None, "Unique Topics": {}}
    for i, article in enumerate(articles):
        topics = extract_topics(article["Summary"], top_n=3)
        topic_overlap["Unique Topics"][f"Article {i+1}"] = topics[:2]

    topic_overlap["Common Topics"] = find_common_topics(topic_overlap["Unique Topics"])

    # Determine final sentiment analysis
    final_sentiment = determine_final_sentiment(sentiment_distribution, avg_score)

    return {
        "Sentiment Distribution": dict(sentiment_distribution),
        "Average Sentiment Score": avg_score,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap,
        "Final Sentiment Analysis": final_sentiment
    }