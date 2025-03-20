from gtts import gTTS
from deep_translator import GoogleTranslator

def generate_hindi_tts(report, articles, output_file="output.mp3"):
    """
    Converts the analysis report into Hindi speech and saves it as an MP3 file.

    Args:
        report (dict): The comparative analysis report.
        articles (list): List of articles with their summaries and sentiments.
        output_file (str): The name of the output MP3 file.

    Returns:
        str: Path to the generated MP3 file.
    """
    try:
        # Initialize the translator
        translator = GoogleTranslator(source='en', target='hi')

        # Start with the topic name, summaries, and sentiments
        hindi_summary = "न्यूज़ रिपोर्ट का विश्लेषण:\n\n"
        for i, article in enumerate(articles, start=1):
            # Translate title and summary to Hindi
            title_hindi = translator.translate(article['Title'])
            summary_hindi = translator.translate(article['Summary'])

            hindi_summary += f"लेख {i}:\n"
            hindi_summary += f"शीर्षक: {title_hindi}।\n"
            hindi_summary += f"सारांश: {summary_hindi}।\n"
            hindi_summary += f"भावना: {article['Sentiment']}।\n\n"

        # Add comparative analysis
        hindi_summary += "तुलनात्मक विश्लेषण:\n\n"
        sentiment_dist = report["Sentiment Distribution"]
        hindi_summary += f"सकारात्मक लेख: {sentiment_dist.get('Positive', 0)}।\n"
        hindi_summary += f"नकारात्मक लेख: {sentiment_dist.get('Negative', 0)}।\n"
        hindi_summary += f"तटस्थ लेख: {sentiment_dist.get('Neutral', 0)}।\n\n"

        hindi_summary += "लेखों के बीच तुलना:\n"
        for comparison in report["Coverage Differences"]:
            # Translate comparison and impact to Hindi
            comparison_hindi = translator.translate(comparison['Comparison'])
            impact_hindi = translator.translate(comparison['Impact'])
            hindi_summary += f"{comparison_hindi}।\n"
            hindi_summary += f"प्रभाव: {impact_hindi}।\n\n"

        # Add topic overlap
        topic_overlap = report["Topic Overlap"]
        if topic_overlap["Common Topics"]:
            common_topic_hindi = translator.translate(topic_overlap["Common Topics"])
            hindi_summary += f"सामान्य विषय: {common_topic_hindi}।\n\n"
        else:
            hindi_summary += "कोई सामान्य विषय नहीं पाया गया।\n\n"

        hindi_summary += "प्रत्येक लेख के अनूठे विषय:\n"
        for article, topics in topic_overlap["Unique Topics"].items():
            unique_topics_hindi = [translator.translate(topic) for topic in topics]
            hindi_summary += f"{article}: {', '.join(unique_topics_hindi)}।\n"

        # Add final sentiment analysis
        final_sentiment_hindi = translator.translate(report['Final Sentiment Analysis'])
        hindi_summary += "\nअंतिम भावना विश्लेषण:\n"
        hindi_summary += f"{final_sentiment_hindi}।\n"

        # Generate Hindi speech
        tts = gTTS(hindi_summary, lang="hi")
        tts.save(output_file)
        print(f"[INFO] Audio file saved as {output_file}")
        return output_file

    except Exception as e:
        print(f"[ERROR] Failed to generate TTS: {e}")
        return None