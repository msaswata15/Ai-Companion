from app.utils import genai

def generate_cheat_sheet(topic: str) -> str:
    """Generate a concise cheat sheet for the given algorithm topic."""
    response = genai.chat.create(
        model="models/chat-bison-001",
        messages=[{"author": "user", "content": f"Create a cheat sheet for {topic}."}],
        temperature=0.5,
    )
    return response.last
