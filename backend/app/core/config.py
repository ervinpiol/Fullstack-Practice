import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL")

settings = Settings()
