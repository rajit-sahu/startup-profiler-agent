import logging
import os
from dotenv import load_dotenv
from supabase import create_client, Client

logger = logging.getLogger(__name__)
load_dotenv(".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "startups"

def already_processed(domain: str) -> bool:
    try:
        result = supabase.table(TABLE_NAME).select("domain").eq("domain", domain).execute()
        return len(result.data) > 0
    except Exception as e:
        logger.error(f"Error checking Supabase for domain {domain}: {e}")
        return False

def save_result(domain: str, profile: dict):
    record = {"domain": domain, **profile}
    try:
        supabase.table(TABLE_NAME).insert(record).execute()
        logger.info(f"Saved profile for {domain} to Supabase.")
    except Exception as e:
        logger.error(f"Failed to save profile to Supabase for {domain}: {e}")
        raise