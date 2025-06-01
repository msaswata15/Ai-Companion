from app.utils import genai

def evaluate_answer(question: str, answer: str) -> dict:
    """Send the question and user's answer to Gemini, return feedback and score."""
    prompt = f"""
    You are a technical interview evaluator. Given the following question and answer, give:

    A score from 0 to 10 for technical correctness, completeness, and clarity.

    A short explanation of the strengths.

    A short list of improvements.

    Question:
    {question}

    Answer:
    {answer}

    Respond in this format:
    Score: <score>/10
    Strengths:

    ...
    Improvements:

    ...
        Correct answer:

    ...

    """
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return {"raw": response.text}