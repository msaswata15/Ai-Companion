from app.utils import genai

def extract_topics_from_text(resume_text: str, job_description: str = None) -> list[str]:
    """
    Extracts a list of the top 5–7 technical or algorithmic topics based on the resume and job description.
    """
    combined_text = resume_text
    if job_description:
        combined_text += f"\n\nJob Description:\n{job_description}"

    prompt = f"""
    Extract a list of the top 5–7 most important technical or algorithmic topics mentioned or implied in the following text.

    Text:
    {combined_text}

    Only return a comma-separated list of topics (like Dynamic Programming, Greedy Algorithms, SQL, etc.) with no explanation.
    """
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    topics_text = response.text if hasattr(response, "text") else str(response)
    return [topic.strip() for topic in topics_text.split(',') if topic.strip()]


def generate_cheat_sheet(topic: str, job_description: str = None) -> str:
    """
    Generate a concise, tailored cheat sheet on a given topic, considering the job description for relevance.
    """
    prompt = f"""
    Create a concise, clear cheat sheet on the topic: {topic}.
    """
    if job_description:
        prompt += f"\n\nThis is the relevant job description. Tailor the cheat sheet to emphasize concepts, code, and tips most useful for this job:\n{job_description}"

    prompt += """
    Include:
    - Key concepts
    - Code examples (in Python)
    - Common use cases
    - Pitfalls or misconceptions
    - Tabular breakdown or tips (if applicable)
    - Some interview questions and answers related to this topic

    Format it using markdown-style headings and bullet points.
    """
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else str(response)


def generate_combined_cheat_sheet(resume_text: str, job_description: str = None) -> str:
    """
    Generate cheat sheets for top extracted topics from resume and JD combined.
    """
    topics = extract_topics_from_text(resume_text, job_description)
    combined_text = job_description if job_description else ""
    all_sheets = ""

    for topic in topics:
        all_sheets += f"# Cheat Sheet: {topic}\n\n"
        all_sheets += generate_cheat_sheet(topic, combined_text)
        all_sheets += "\n\n---\n\n"

    return all_sheets
