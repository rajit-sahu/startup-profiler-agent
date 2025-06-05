import logging
from app.agent import agent_executor
from langchain_core.messages import HumanMessage
from app.supabase import already_processed, save_result
from urllib.parse import urlparse
import json
import re

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No JSON object found in agent response.")

def get_domain(url: str):
    return urlparse(url).netloc.replace("www.", "")

def main():
    try:
        url = ("Notion.so")
        if not url.startswith("http"):
            url = "https://" + url
        domain = get_domain(url)

        logger.info(f"Processing domain: {domain}")
        if already_processed(domain):
            logger.info(f"{domain} already processed. Exiting.")
            return

        logger.info(f"Invoking agent on: {url}")
        result = agent_executor.invoke({ "input": url })
        final_response = result["messages"][-1].content
        logger.info("Agent returned, parsing JSON…")

        print("\n=== Startup Profile JSON ===\n")
        print(final_response)

        parsed = extract_json(final_response)
        save_result(domain, parsed)
        logger.info(f"Saved profile for {domain} to Supabase.")

    except Exception as e:
        logger.error(f"Unhandled error in main: {e}", exc_info=True)

if __name__ == "__main__":
    main()