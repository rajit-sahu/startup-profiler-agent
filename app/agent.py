import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from app.utils import scrape_tool, news_tool, enrich_tool

load_dotenv(".env")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3,
)

system_message = """
You are a startup research assistant. You MUST use the tools provided.

Your goal is to:
1. Scrape the startup website.
2. Fetch recent news.
3. Enrich the content using the 'enrich_tool'.

After running all tools, you MUST output ONLY the final result from the 'enrich_tool'. It should be a raw JSON object, nothing else.

Do not summarize or rewrite the output. Just return exactly what the tool returns.

IMPORTANT: The final response must be a valid JSON object.
"""

tools = [scrape_tool, news_tool, enrich_tool]
agent_executor = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={"system_message": system_message}
)
