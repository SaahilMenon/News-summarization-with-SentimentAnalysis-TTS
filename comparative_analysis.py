from collections import Counter
from keybert import KeyBERT
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import statistics
import nltk

# Download NLTK data (if not already downloaded)
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize KeyBERT model for keyword extraction
kw_model = KeyBERT()

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def extract_topics(text, top_n=3):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    normalized_keywords = [lemmatizer.lemmatize(keyword[0].lower()) for keyword in keywords]
    return normalized_keywords

def find_common_topics(unique_topics):
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

    Args:
        sentiment_distribution (dict): Distribution of sentiments (Positive, Negative, Neutral).
        avg_score (float): Average sentiment score.

    Returns:
        str: Final sentiment analysis summary.
    """
    positive_count = sentiment_distribution.get("Positive", 0)
    negative_count = sentiment_distribution.get("Negative", 0)
    neutral_count = sentiment_distribution.get("Neutral", 0)

    if positive_count > negative_count and avg_score > 0.6:
        return "Overall sentiment is mostly positive."
    elif negative_count > positive_count and avg_score < 0.4:
        return "Overall sentiment is mostly negative."
    else:
        return "Overall sentiment is neutral."

def comparative_analysis(articles):
    sentiment_distribution = Counter(article["Sentiment"] for article in articles)
    scores = [article.get("Sentiment Score", 0.0) for article in articles if isinstance(article.get("Sentiment Score", 0.0), (int, float))]
    avg_score = round(statistics.mean(scores), 3) if scores else 0.0

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

    topic_overlap = {"Common Topics": None, "Unique Topics": {}}
    for i, article in enumerate(articles):
        topics = extract_topics(article["Summary"], top_n=3)
        topic_overlap["Unique Topics"][f"Article {i+1}"] = topics[:2]

    topic_overlap["Common Topics"] = find_common_topics(topic_overlap["Unique Topics"])

    final_sentiment = determine_final_sentiment(sentiment_distribution, avg_score)

    return {
        "Sentiment Distribution": dict(sentiment_distribution),
        "Average Sentiment Score": avg_score,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap,
        "Final Sentiment Analysis": final_sentiment
    }