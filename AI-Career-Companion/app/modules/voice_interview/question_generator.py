from app.utils import genai

def generate_question_for_topic(topic: str) -> str:
    """Generate an interview-style question for a specific topic."""
    prompt = f"""
    Create a technical interview question suitable for a student on the topic: {topic}.
    Make sure it is clear and concise.
    """
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()