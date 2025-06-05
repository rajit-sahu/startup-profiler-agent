import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "startups"


def already_processed(domain: str) -> bool:
    result = supabase.table(TABLE_NAME).select("domain").eq("domain", domain).execute()
    return len(result.data) > 0


def save_result(domain: str, profile: dict):
    record = {"domain": domain, **profile}
    supabase.table(TABLE_NAME).insert(record).execute()
