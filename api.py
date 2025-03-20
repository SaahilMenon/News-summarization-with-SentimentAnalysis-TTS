from flask import Flask, request, jsonify
from scraping import fetch_bing_news
from sentiment import analyze_articles
from comparative_analysis import comparative_analysis
from tts import generate_hindi_tts

app = Flask(__name__)

@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    company_name = request.args.get('company_name')
    limit = int(request.args.get('limit', 10))
    articles = fetch_bing_news(company_name, limit)
    return jsonify({"Articles": articles})

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    articles = request.json.get('articles', [])
    analyzed_articles = analyze_articles(articles)
    return jsonify({"Articles": analyzed_articles})

@app.route('/comparative_analysis', methods=['POST'])
def perform_comparative_analysis():
    articles = request.json.get('articles', [])
    report = comparative_analysis(articles)
    return jsonify({"Comparative Analysis": report})

@app.route('/generate_tts', methods=['POST'])
def generate_tts():
    report = request.json.get('report', {})
    articles = request.json.get('articles', [])
    output_file = "analysis_report.mp3"
    try:
        generate_hindi_tts(report, articles, output_file=output_file)
        return jsonify({"message": "TTS generated successfully", "file": output_file})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)