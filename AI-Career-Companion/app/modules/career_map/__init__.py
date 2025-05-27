from app.utils import genai

def generate_career_map(profile: str) -> str:
    """Suggest career paths with day-in-the-life details."""
    response = genai.chat.create(
        model="models/chat-bison-001",
        messages=[{"author": "user", "content": f"Based on my profile {profile}, suggest career paths"}],
        temperature=0.6,
    )
    return response.last
