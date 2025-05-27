from app.modules.generate_doc import generate_resume

def test_generate_resume_returns_string():
    result = generate_resume("Test job description")
    assert isinstance(result, str)
    assert len(result) > 0
