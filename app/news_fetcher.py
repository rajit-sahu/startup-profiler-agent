import logging
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
load_dotenv(dotenv_path=".env")

def fetch_latest_news(company_name):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        logger.error("SERPAPI_KEY is missing in .env")
        raise ValueError("SERPAPI_KEY is missing in .env")

    params = {
        "engine": "google_news",
        "q": company_name,
        "api_key": api_key,
        "gl": "sg",
        "hl": "en"
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        articles = results.get("news_results", [])[:5]
    except Exception as e:
        logger.error(f"Error fetching news for {company_name}: {e}")
        return []

    parsed = []
    for a in articles:
        parsed.append({
            "title": a.get("title", ""),
            "source": a.get("link", ""),
            "date": a.get("date", "")
        })
    return parsed