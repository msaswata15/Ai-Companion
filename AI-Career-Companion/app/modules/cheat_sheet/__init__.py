from app.utils import genai

def extract_topics_from_text(text: str) -> list[str]:
   
    prompt = f"""
    Extract a list of the top 5–7 most important technical or algorithmic topics mentioned or implied in the following text.

    Text:
    {text}

    Only return a comma-separated list of topics (like Dynamic Programming, Greedy Algorithms, SQL, etc.) with no explanation.
    """
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    topics_text = response.text if hasattr(response, "text") else str(response)
    return [topic.strip() for topic in topics_text.split(',') if topic.strip()]

def generate_cheat_sheet(topic: str) -> str:

    prompt = f"""
    Create a concise, clear cheat sheet on the topic: {topic}.

    Include:

    Key concepts

    Code examples (in Python)

    Common use cases

    Pitfalls or misconceptions

    Tabular breakdown or tips (if applicable)

    Format it using markdown-style headings and bullet points.
    """
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else str(response)

def generate_combined_cheat_sheet(text: str) -> str:
    """Extract topics from resume + JD and generate combined cheat sheets."""
    topics = extract_topics_from_text(text)
    combined = ""
    for topic in topics:
        combined += f"# Cheat Sheet: {topic}\n\n"
        combined += generate_cheat_sheet(topic)
        combined += "\n\n---\n\n"
    return combined