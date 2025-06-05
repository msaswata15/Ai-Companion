from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    google_api_key: str
    assembly_api_key: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create instance of settings
settings = Settings()
