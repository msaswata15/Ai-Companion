import os
import redis
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import google.generativeai as genai
# ——— Pydantic Settings import from pydantic-settings ———

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    google_api_key: str
    assembly_api_key: str
    database_url: str = "sqlite:///./app.db"    # fallback
    redis_url: str = "redis://localhost:6379"

settings = Settings()

# ——— Configure Gemini API key ———
genai.configure(api_key=settings.google_api_key)

# ——— Database setup ———
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = sqlalchemy.create_engine(
    settings.database_url,
    connect_args=connect_args if connect_args else None
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ——— Redis client ———
redis_client = redis.from_url(settings.redis_url, decode_responses=True)
