from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from models.request_models import JobPreferences
from models.response_models import CareerRecommendation, JobMatch
from services.career_logic import (
    process_resume,
    generate_recommendations,
    search_jobs,
    generate_cheat_sheet
)

router = APIRouter()

@router.post("/upload-resume", response_model=dict)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process a resume file"""
    try:
        resume_text = await process_resume(file)
        return {"success": True, "resume_text": resume_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/recommendations", response_model=CareerRecommendation)
async def get_recommendations(preferences: JobPreferences):
    """Get career recommendations based on preferences"""
    try:
        recommendations = await generate_recommendations(preferences)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/search-jobs", response_model=list[JobMatch])
async def search_jobs_route(
    keywords: str = Form(...),
    location: Optional[str] = Form(None)
):
    """Search for matching jobs"""
    try:
        jobs = await search_jobs(keywords, location)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cheat-sheet")
async def generate_cheat_sheet_route(
    topic: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Generate a technical cheat sheet"""
    try:
        sheet = await generate_cheat_sheet(topic, context)
        return {"content": sheet}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))