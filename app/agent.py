import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from tools import scrape_tool, news_tool, enrich_tool

load_dotenv(".env")

model = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    google_api_key = os.getenv("GEMINI_API_KEY")
)

tools = [scrape_tool, news_tool, enrich_tool]
agent_executor = create_react_agent(model, tools)