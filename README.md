# Startup Profiler Agent

An intelligent agent that analyzes any startup or company by scraping its website, fetching recent news article, then enriching the data using gemini, and storing the structured results in supabase.

## Tech Stack

- **Language**: Python 3.10+
- **LLM**: Google Gemini (via REST API)
- **Database**: Supabase (PostgreSQL)
- **Web Search**: SerpAPI
- **Scraping**: BeautifulSoup + Requests
- **Containerization**: Docker + Docker Compose
- **Framework**: LangChain (for LLM prompt handling)

## Features

- Scrape homepage for:
  - Page title
  - Meta description
  - H1/H2 tags
  - Outbound links
  - Main content
- Fetch recent news using SerpAPI
- Enrich data with Google Gemini:
  - Summary
  - Industry, target audience
  - Problem solved, competitors
  - News summary
- Store entries in Supabase (skip if already exists)

## Setup

### 1. Clone Repo

```bash
git clone https://github.com/your-username/startup-profiler-agent.git
cd startup-profiler-agent
