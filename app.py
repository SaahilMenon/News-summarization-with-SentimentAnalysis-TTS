from flask import Flask, jsonify
from flask_cors import CORS
import api

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "News Summarization and TTS API is running!"})

app.register_blueprint(api.api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
