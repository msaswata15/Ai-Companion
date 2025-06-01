from pydantic import BaseModel
from typing import List, Optional

class JobMatch(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    match_score: Optional[float] = None

class CareerRecommendation(BaseModel):
    career_paths: List[str]
    recommended_skills: List[str]
    job_matches: List[JobMatch]
    improvement_suggestions: List[str]