import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"  # Change this if deploying

st.title("📢 News Sentiment & TTS Analyzer")
st.markdown("Analyze news articles, perform sentiment analysis, comparison and generate Hindi TTS reports.")

company = st.text_input("🔍 Enter company name:", placeholder="Tesla, Apple, Microsoft..")

news_data = None  # Store analyzed news data globally

def fetch_analysis():
    global news_data
    with st.spinner("Fetching and analyzing news..."):
        response = requests.get(f"{API_URL}/analyze", params={"company": company})
        if response.status_code == 200:
            news_data = response.json()
            st.subheader(f"📰 News Analysis for {company}")
            for idx, article in enumerate(news_data["Articles"], start=1):
                st.markdown(f"### {idx}) Title: {article['Title']}")
                st.write(f"**Summary:** {article['Summary']}")
                st.write(f"**Sentiment:** {article['Sentiment']} 
                st.write(f"**Topics:** {', '.join(article.get('Topics', [])) if article.get('Topics') else 'None'}")
                st.write(f"**URL:** [Read more]({article['URL']})")
                st.markdown("---")
            
            st.subheader("📊 Comparative Sentiment Analysis")
            st.json(news_data["Comparative Sentiment Score"])
        else:
            st.error("❌ Failed to fetch analysis.")

if st.button("📊 Analyze News"):
    fetch_analysis()

if st.button("🎙️ Generate TTS Report"):
    if news_data:
        with st.spinner("Generating TTS report..."):
            response = requests.get(f"{API_URL}/tts", params={"company": company})
            if response.status_code == 200:
                data = response.json()
                if "Audio" in data:
                    st.subheader("🔊 Hindi TTS Report")
                    st.audio(data["Audio"], format="audio/mp3")
                else:
                    st.error("❌ TTS generation failed.")
            else:
                st.error("❌ Failed to generate TTS.")
    else:
        st.error("⚠️ Please analyze news first before generating TTS.")