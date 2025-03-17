import requests
from bs4 import BeautifulSoup

def fetch_news(company_name):
    url = f"https://news.google.com/search?q={company_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch news"}

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    
    for item in soup.select("article")[:10]:  # Limit to 10 articles
        title = item.select_one("h3").text if item.select_one("h3") else "No Title"
        link = "https://news.google.com" + item.select_one("a")["href"][1:]
        articles.append({"title": title, "link": link})
    
    return articles
