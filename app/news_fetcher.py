import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.template")

def fetch_latest_news(company_name):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SERPAPI_KEY is missing in .env")
    
    params = {
        "engine": "google_news",
        "q": company_name,
        "api_key":api_key,
        "gl": "sg",
        "hl": "en"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    articles = results.get("news_results")[:5]
    
    parsed = []
    
    for a in articles:
        parsed.append({
            "title": a.get("title", ""),
            "source": a.get("link", ""),
            "date": a.get("date", "")
        })
        
    return parsed