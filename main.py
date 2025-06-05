from app.scraper import scrape_site
from app.news_fetcher import fetch_latest_news
from app.gemini_wrapper import enrich_data

if __name__ == "__main__":
    data = scrape_site("https://notion.so")
    news = fetch_latest_news("Notion.so")
    profile = enrich_data(data, news)
    print(data)
    print(news)
    print(profile)