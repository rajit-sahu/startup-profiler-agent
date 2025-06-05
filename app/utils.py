import json
import logging
from langchain_core.tools import tool
from app.scraper import scrape_site
from app.news_fetcher import fetch_latest_news
from app.gemini_wrapper import enrich_data
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

@tool
def scrape_tool(url: str) -> dict:
    """Scrape a website and return structured content."""
    return scrape_site(url)

@tool
def news_tool(url: str) -> list:
    """Fetch latest news headlines using the company name from a URL."""
    hostname = urlparse(url).hostname or ""
    name = hostname.replace("www.", "").split(".")[0].capitalize()
    return fetch_latest_news(name)

@tool
def enrich_tool(combined_json: str) -> dict:
    """
    Enrich data using Gemini. 
    Expect `combined_json` to be a JSON string with two keys:
      - "scraped": <the entire dict returned by scrape_tool>
      - "news": <the list returned by news_tool>

    Example of combined_json:
      '{"scraped": {...}, "news": [...]}'
    """
    try:
        payload = json.loads(combined_json)
    except json.JSONDecodeError as e:
        logger.error(f"enrich_tool: invalid JSON input: {e}")
        raise

    scraped = payload.get("scraped", {})
    news = payload.get("news", [])
    return enrich_data(scraped, news)