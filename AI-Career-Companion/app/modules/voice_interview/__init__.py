from .transcribe import transcribe_audio
from .evaluate import evaluate_answer
from .topic_extractor import extract_interview_topics
from .question_generator import generate_question_for_topic
from .record_audio import save_uploaded_audio

def get_questions_from_resume_and_jd(resume_text: str, jd_text: str) -> list[dict]:
    """Extract topics from text and generate questions."""
    full_text = f"{resume_text}\n\n{jd_text}"
    topics = extract_interview_topics(full_text)
    return [{"topic": t, "question": generate_question_for_topic(t)} for t in topics]

def generate_feedback_from_audio(file_path: str, question: str) -> dict:
    """Given an audio file and the question, transcribe and evaluate it."""
    transcript = transcribe_audio(file_path)
    feedback = evaluate_answer(question, transcript)
    return {
    "transcript": transcript,
    "feedback": feedback["raw"]
    }