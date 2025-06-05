# tools for langchain
from langchain_core.tools import tool
from app.scraper import scrape_site
from app.news_fetcher import fetch_latest_news
from app.gemini_wrapper import enrich_data
from urllib.parse import urlparse


@tool
def scrape_tool(url: str) -> dict:
    """Scrape a website and return structured page content."""
    return scrape_site(url)


@tool
def news_tool(url: str) -> list:
    """Fetch latest news headlines using the company name from a URL."""
    hostname = urlparse(url).hostname or ""
    name = hostname.replace("www.", "").split(".")[0].capitalize()
    return fetch_latest_news(name)


@tool
def enrich_tool(scraped_and_news: dict) -> dict:
    """Enrich scraped + news data using Gemini to build a company profile."""
    return enrich_data(input["scraped"], input["news"])
