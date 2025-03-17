from flask import Blueprint, request, jsonify
from scraping import fetch_news
from sentiment import analyze_sentiment
from comparative import comparative_analysis
from tts import generate_tts

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/news', methods=['GET'])
def get_news():
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Company name required"}), 400

    articles = fetch_news(company)
    return jsonify({"company": company, "articles": articles})

@api_blueprint.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text data required"}), 400

    sentiment = analyze_sentiment(data["text"])
    return jsonify({"sentiment": sentiment})

@api_blueprint.route('/comparative', methods=['POST'])
def compare_news():
    data = request.get_json()
    if not data or "articles" not in data:
        return jsonify({"error": "Articles data required"}), 400

    result = comparative_analysis(data["articles"])
    return jsonify(result)

@api_blueprint.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text data required"}), 400

    file_path = generate_tts(data["text"])
    return jsonify({"audio_url": file_path})
