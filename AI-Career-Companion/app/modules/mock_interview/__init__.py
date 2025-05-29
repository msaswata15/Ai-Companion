from app.utils import genai

def run_mock_interview(prompt: str) -> str:
    """Run a mock interview Q&A session with feedback."""
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(f"Interview me on algorithms: {prompt}")
    return response.text if hasattr(response, 'text') else str(response)
