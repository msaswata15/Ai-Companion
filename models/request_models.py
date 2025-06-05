from pydantic import BaseModel
from typing import Optional, List

class JobPreferences(BaseModel):
    keywords: str
    location: Optional[str] = None
    remote: Optional[bool] = False
    skills: Optional[List[str]] = []
    experience_years: Optional[int] = None

class ResumeUpload(BaseModel):
    file_content: bytes
    filename: str