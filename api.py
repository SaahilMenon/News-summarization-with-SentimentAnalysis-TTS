from fastapi import FastAPI
from sentiment import get_news_articles_with_sentiment
from comparative_analysis import comparative_analysis
from tts import generate_hindi_tts
import json

app = FastAPI()

@app.get("/analyze")
def analyze(company: str, limit: int = 10):
    """
    Fetches news articles, performs sentiment analysis, and runs comparative analysis.
    """
    news_data = get_news_articles_with_sentiment(company, limit)
    
    if not news_data.get("Articles"):
        return {"error": "No articles found"}
    
    comparative_data = comparative_analysis(news_data["Articles"])
    
    structured_output = {
        "Company": company,
        "Articles": news_data["Articles"],
        "Comparative Sentiment Score": comparative_data
    }
    
    return structured_output

@app.get("/tts")
def generate_tts(company: str):
    """
    Generates Hindi TTS from the sentiment analysis report.
    """
    news_data = get_news_articles_with_sentiment(company, limit=10)
    if not news_data.get("Articles"):
        return {"error": "No articles found"}
    
    comparative_data = comparative_analysis(news_data["Articles"])
    audio_path = generate_hindi_tts(comparative_data, news_data["Articles"])
    
    return {"Audio": audio_path}
