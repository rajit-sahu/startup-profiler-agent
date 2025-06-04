import google.generativeai as genai
import os
from pydantic import BaseModel
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path=".env.template")
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

# making a structured schema
class company_profile(BaseModel):
    company_appeal: str
    industry: str
    target_audience: str
    problems_solved: str
    pot_competitors: list[str]
    news_summary: str

def build_prompt(scraper_data, news_articles):
    prompt = f"""
    You are a business analyst specializing in startups.
        
    A startup has the following data on their website:
    - Title: {scraper_data.get("title", "")}
    - Meta description: {scraper_data.get("meta_description", "")}
    - H1 tags: {scraper_data.get("h1_tags", [])}
    - H2 tags: {scraper_data.get("h2_tags", [])}
    - Outbound links: {scraper_data.get("outbound_links", [])}
    - Content snippet: {scraper_data.get("content", '')}
    
    Recent News about the given startup is:   
    """
    for i, article in enumerate(news_articles, 1):
        prompt += f"\n  {i}. {article['title']} — {article['source']} ({article['date']})"

    prompt += """
    Return a JSON object with the following fields:
    {
    "company_appeal": "...", (what the company does (100 word summary))
    "industry": "...", (what industry is the company in)
    "target": "...", (who is the target audience)
    "problems_solved": "...", (what key problems does the company solve)
    "competitors": ["...", "..."], (suggest 2, 3 potentional competitors for the company)
    "news_summary": "..." (Summarize the latest news into a short paragraph)
    }
    """
    return prompt.strip()

def enrich_data(scraper_data, news_articles): 
    prompt = build_prompt(scraper_data, news_articles)
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt,
        config = {
                    "responses_mime_type":"application/json",
                    "response_schema": list[company_profile]
                    }
        )
    return response