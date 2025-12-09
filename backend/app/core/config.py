import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    REDIS_URL: str = os.getenv("REDIS_URL")

settings = Settings()
