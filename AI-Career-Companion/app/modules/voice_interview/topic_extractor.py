from app.utils import genai

def extract_interview_topics(text: str) -> list[str]:
    """Extract key technical interview topics from resume + JD text."""
    prompt = f"""
    Given the following resume and job description text, extract the 5 to 7 most relevant technical topics or concepts that a candidate should be prepared to answer in an interview. Focus on data structures, algorithms, AI/ML tools, libraries, platforms, and key skills.

    Text:
    {text}

    Output only a comma-separated list of topics.
    """
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    topics = response.text.split(",")
    return [t.strip() for t in topics if t.strip()]