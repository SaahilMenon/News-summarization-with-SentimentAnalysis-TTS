import streamlit as st
import requests

# Backend API URLs
BASE_URL = "http://127.0.0.1:5000"

# Streamlit app
st.title("News Summarization and Sentiment Analysis")
st.write("Analyze news articles, perform sentiment analysis, and generate a Hindi audio summary.")

# Input for topic or company name
topic = st.text_input("Enter a company name:", placeholder="e.g., Tesla, Apple")
limit = st.slider("Number of articles to fetch:", min_value=1, max_value=10, value=5)

if st.button("Analyze"):
    if not topic.strip():
        st.error("Please enter a valid topic or company name.")
    else:
        # Fetch news articles
        st.info("Fetching news articles...")
        try:
            response = requests.get(f"{BASE_URL}/fetch_news", params={"company_name": topic, "limit": limit})
            news_data = response.json()
            articles = news_data.get("Articles", [])

            if not articles:
                st.warning(f"No articles found for '{topic}'. Please try a different topic.")
            else:
                if len(articles) < limit:
                    st.warning(f"Only {len(articles)} articles were found for '{topic}'.")

                # Display the fetched articles
                st.write("Fetched Articles:")
                for idx, article in enumerate(articles, start=1):
                    st.write(f"**Article {idx}:**")
                    st.write(f"**Title:** {article.get('Title', 'N/A')}")
                    st.write(f"**Summary:** {article.get('Summary', 'N/A')}")
                    st.write(f"**Source and Time:** {article.get('Source and Time', 'N/A')}")
                    st.write(f"**URL:** {article.get('URL', 'N/A')}")
                    st.write("---")

                # Perform sentiment analysis
                st.info("Performing sentiment analysis...")
                response = requests.post(f"{BASE_URL}/analyze_sentiment", json={"articles": articles})
                analyzed_data = response.json()
                articles = analyzed_data.get("Articles", [])
                news_data["Sentiment Analysis"] = articles

                # Perform comparative analysis
                st.info("Performing comparative analysis...")
                response = requests.post(f"{BASE_URL}/comparative_analysis", json={"articles": articles})
                comparative_report = response.json().get("Comparative Analysis", {})
                news_data["Comparative Analysis"] = comparative_report
                
                 # Perform final sentiment analysis
                st.info("Performing final sentiment analysis...")
                response = requests.post(f"{BASE_URL}/analyze_sentiment", json={"articles": articles})
                final_sentiment_data = response.json()
                final_articles = final_sentiment_data.get("Articles", [])
                news_data["Final Sentiment Analysis"] = final_articles


                # Display the comparative analysis report
                st.subheader("Full Analysis Report")
                st.json(news_data)

                # Generate Hindi TTS
                st.info("Generating Hindi audio summary...")
                response = requests.post(f"{BASE_URL}/generate_tts", json={"report": comparative_report, "articles": articles})
                if response.status_code == 200:
                    st.success("Hindi audio summary generated successfully!")
                    st.audio("analysis_report.mp3", format="audio/mp3")
                else:
                    st.error("Failed to generate the Hindi audio summary.")
        except Exception as e:
            st.error(f"An error occurred: {e}")