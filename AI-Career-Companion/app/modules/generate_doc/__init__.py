from app.utils import genai
from app.modules.generate_doc.resume_parser import extract_resume_details_from_pdf

def generate_resume(job_description: str, resume_details: dict = None) -> str:
    """Use Gemini to transform JD and resume details into bullet-point resume."""
    prompt = f"Generate a resume from: {job_description}"
    if resume_details and 'raw_text' in resume_details:
        prompt += f"\n\nHere is my current resume:\n{resume_details['raw_text']}"
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response)

def generate_cover_letter(job_description: str, resume_details: dict = None) -> str:
    """Use Gemini to write a cover letter tailored to the JD and resume details."""
    prompt = f"Write a cover letter for: {job_description}"
    if resume_details and 'raw_text' in resume_details:
        prompt += f"\n\nHere is my current resume:\n{resume_details['raw_text']}"
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response)
