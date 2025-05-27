from app.utils import genai

def run_mock_interview(prompt: str) -> str:
    """Run a mock interview Q&A session with feedback."""
    response = genai.chat.create(
        model="models/codechat-bison-001",
        messages=[{"author": "user", "content": f"Interview me on algorithms: {prompt}"}],
        temperature=0.3,
    )
    return response.last
