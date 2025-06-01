from fastapi import UploadFile
import pdfplumber
from app.utils import genai
from typing import List, Optional
import aiofiles
import tempfile
import os

async def process_resume(file: UploadFile) -> str:
    """Process uploaded resume and extract text"""
    if not file.filename.endswith('.pdf'):
        raise ValueError("Only PDF files are supported")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        with pdfplumber.open(tmp_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        return text
    finally:
        os.unlink(tmp_path)

async def generate_recommendations(preferences) -> dict:
    """Generate career recommendations based on preferences"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = f"""
    Based on these preferences:
    Keywords: {preferences.keywords}
    Location: {preferences.location or 'Any'}
    Skills: {', '.join(preferences.skills) if preferences.skills else 'Not specified'}
    Experience: {preferences.experience_years or 'Not specified'} years

    Suggest career paths and improvements.
    """
    response = model.generate_content(prompt)
    suggestions = response.text if hasattr(response, 'text') else str(response)
    
    return {
        "career_paths": ["Data Scientist", "ML Engineer"],  # Example
        "recommended_skills": ["Python", "TensorFlow"],
        "job_matches": [],
        "improvement_suggestions": [suggestions]
    }

async def search_jobs(keywords: str, location: Optional[str] = None) -> List[dict]:
    """Search for matching jobs using external APIs"""
    from app.utils import fetch_jobs_remotive, fetch_jobs_adzuna
    
    jobs = []
    if location:
        jobs.extend(await fetch_jobs_adzuna(keywords, location=location))
    else:
        jobs.extend(await fetch_jobs_remotive(keywords, location='India'))
    
    return jobs

async def generate_cheat_sheet(topic: str, context: Optional[str] = None) -> str:
    """Generate a technical cheat sheet for a topic"""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    prompt = f"""Create a concise cheat sheet for: {topic}"""
    if context:
        prompt += f"\nContext: {context}"
    
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response)