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
    assembly_api_key: str  # <-- must be lowercase with underscores
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

def fetch_jobs_remotive(keywords: str, limit: int = 5, location: str = ""):
    """Fetch jobs from Remotive API matching the given keywords and location."""
    import requests
    url = f"https://remotive.com/api/remote-jobs?search={keywords}"
    if location and location.upper() != "IN":
        url += f"&location={location}"
    elif location.upper() == "IN":
        url += f"&locationdia"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        jobs = resp.json().get('jobs', [])
        return [
            {
                'title': job['title'],
                'company': job['company_name'],
                'location': job['candidate_required_location'],
                'desc': job['description'],
                'url': job['url']
            }
            for job in jobs[:limit]
        ]
    except Exception as e:
        return []

def fetch_jobs_adzuna(keywords: str, location: str = None, limit: int = 10):
    """Fetch jobs from Adzuna API matching the given keywords and location (default India or user's country)."""
    import requests
    import os
    # Use IP geolocation if location is not provided
    if not location:
        try:
            resp = requests.get("https://ipinfo.io/json", timeout=5)
            data = resp.json()
            location = data.get("country", "India")
        except Exception:
            location = "India"
    country = location.lower() if location else "in"
    valid_countries = ["in", "us", "gb", "ca", "au", "de", "fr", "nl", "pl", "ru", "za", "br", "sg", "nz", "cz", "es", "it", "mx", "se", "ch", "at", "be", "fi", "no", "dk", "ie", "ar", "tr", "ae", "hk", "jp", "cn", "pt", "hu", "il", "my", "ro", "sa", "ua", "ve"]
    if country not in valid_countries:
        country = "in"
    APP_ID = os.getenv("58b928ad", "58b928ad")
    APP_KEY = os.getenv("33d7ded694ba1de712c7bd0e7e85817c", "33d7ded694ba1de712c7bd0e7e85817c")
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page={limit}&what={keywords}&where={location}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        jobs = resp.json().get('results', [])
        return [
            {
                'title': job['title'],
                'company': job.get('company', {}).get('display_name', ''),
                'location': job.get('location', {}).get('display_name', ''),
                'desc': job.get('description', ''),
                'url': job['redirect_url']
            }
            for job in jobs
        ]
    except Exception as e:
        return []

def get_user_country():
    """Try to get the user's country using IP geolocation."""
    import requests
    try:
        resp = requests.get("https://ipinfo.io/json", timeout=5)
        data = resp.json()
        return data.get("country", "IN")
    except Exception:
        return "IN"

__all__ = [
    'fetch_jobs_remotive',
    'fetch_jobs_adzuna',
    'get_user_country',
    'genai',
    'redis_client',
    'SessionLocal',
    'settings',
]
