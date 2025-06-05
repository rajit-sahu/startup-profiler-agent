from app.agent import agent_executor
from langchain_core.messages import HumanMessage
from urllib.parse import urlparse
from app.supabase import already_processed, save_result
import json
import re


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No JSON object found in response.")


def get_domain(url: str):
    return urlparse(url).netloc.replace("www.", "")


def main():
    url = input("Enter the company website URL: ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    domain = get_domain(url)

    if already_processed(domain):
        print(f"{domain} already processed. Skipping.")
        return

    result = agent_executor.invoke({"messages": [HumanMessage(content=url)]})
    final = result["messages"][-1].content
    print("\n=== Gemini Enriched Startup Profile ===\n")
    print(final)
    parsed = extract_json(final)
    save_result(domain, parsed)


if __name__ == "__main__":
    main()
