# News_summarization
# News Summarization and Sentiment Analysis Application

## Overview
This application performs news summarization, sentiment analysis, comparative analysis, and generates Hindi audio summaries using text-to-speech. Users can input a company name and receive a structured sentiment report, along with a playable audio output in Hindi.

The solution is designed as part of an internship assignment to demonstrate end-to-end software development involving web scraping, NLP, API design, and deployment.

## Features
- Extract news articles related to a given company using Bing RSS feeds.
- Summarize each article using LexRank extractive summarization.
- Perform sentiment analysis using a transformer-based RoBERTa model.
- Conduct comparative sentiment and topic analysis across articles.
- Generate a Hindi audio summary using gTTS.
- Expose APIs via FastAPI for frontend-backend interaction.
- Simple frontend interface using Streamlit.
- Deployable via Docker or on Hugging Face Spaces.

## Setup Instructions
Follow these steps to run the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/karenrenac/News-Summarization-with-TTS-Application.git
   cd News-Summarization-with-TTS-Application
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend API (FastAPI)**:
   ```bash
   uvicorn api:app --reload
   ```
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive API documentation (Swagger UI).

4. **Run the Frontend (Streamlit)**:
   ```bash
   streamlit run app.py
   ```

### Running with Docker (Optional)
1. **Build Docker Image**:
   ```bash
   docker build -t news-summarizer .
   ```

2. **Run Docker Container**:
   ```bash
   docker run -p 8080:8080 news-summarizer
   ```

## Models and Tools Used
- **Summarization**: LexRank algorithm via `sumy` library.
- **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest` transformer model using Hugging Face transformers.
- **Text-to-Speech (TTS)**: Hindi audio generated using `gTTS`.
- **Topic Analysis**: Extracted using keyword filtering and Sentence-BERT embeddings.
- **Web Scraping**: RSS feed parsing using `feedparser` and `BeautifulSoup`.

## API Details
The backend is developed using FastAPI and exposes endpoints to:
- Accept a company name as input.
- Return structured JSON output with article titles, summaries, sentiment scores, comparative analysis, and topic overlaps.
- Generate Hindi audio summary.

Endpoints are documented at `/docs` via Swagger UI.

## Assumptions & Limitations
- News sources are limited to Bing RSS for simplicity and compatibility.
- Summarization is extractive, not abstractive.
- Hindi audio generation is a basic implementation using `gTTS` and can be enhanced using advanced open-source models.
- The application is optimized for demonstrative purposes and may require scaling strategies for production deployment.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
