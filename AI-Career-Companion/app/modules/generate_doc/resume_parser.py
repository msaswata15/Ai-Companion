import pdfplumber
from typing import Dict

def extract_resume_details_from_pdf(pdf_file) -> Dict[str, str]:
    """Extracts text from a PDF resume and returns a dictionary of details."""
    details = {}
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    # Simple parsing logic (can be improved)
    details['raw_text'] = text
    # TODO: Add more sophisticated parsing for name, skills, etc.
    return details