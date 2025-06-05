from langchain_core.tools import tool
from app.scraper import scrape_site
from app.news_fetcher import fetch_latest_news
from app.gemini_wrapper import enrich_data

@tool
def scrape_tool(url: str) -> dict:
    return scrape_site(url)

@tool
def news_tool(company_name: str) -> list:
    return fetch_latest_news(company_name)

@tool
def enrich_tool(scraped_and_news: dict) -> dict:
    return enrich_data(
        scraped_and_news["scraped"], 
        scraped_and_news["news"]
    )