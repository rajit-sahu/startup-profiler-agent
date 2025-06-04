from app.scraper import scrape_site

if __name__ == "__main__":
    data = scrape_site("https://notion.so")
    print(data)