import google.generativeai as genai
import os
from pydantic import BaseModel
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path=".env")
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

# making a structured schema
class CompanyProfile(BaseModel):
    company_appeal: str
    industry: str
    target_audience: str
    problems_solved: str
    competitors: list[str]
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
    "company_appeal": "...",           // what the company does (max 100 words)
    "industry": "...",                 // what industry is the company in (max 8 words)
    "target_audience": "...",          // who is the target audience (max 50 words)
    "problems_solved": "...",          // what key problems does the company solve (max 40 words)
    "competitors": ["...", "..."],     // 2-3 potential competitors
    "news_summary": "..."              // summarize the latest news (max 100 words)
    }
    """
    return prompt.strip()

def enrich_data(scraper_data, news_articles): 
    prompt = build_prompt(scraper_data, news_articles)
    response = model.generate_content(
        contents=prompt,
        generation_config = {
                    "response_mime_type":"application/json",
                    "response_schema": CompanyProfile
                    }
        )
    return response.parsed