from dotenv import load_dotenv
import os
from supabase import create_client, Client

from litemultiagent.core.config import LiteMultiAgentLogger

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BING_API_KEY = os.getenv("BING_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if SUPABASE_URL and SUPABASE_ANON_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    except Exception as e:
        supabase = None
        LiteMultiAgentLogger.error(f"Failed to initialize Supabase client: {e}")
else:
    supabase = None