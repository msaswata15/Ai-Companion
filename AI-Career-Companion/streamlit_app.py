import os
import streamlit as st
from app.modules.generate_doc import generate_resume, generate_cover_letter
from app.modules.mock_interview import run_mock_interview
from app.modules.cheat_sheet import generate_cheat_sheet
from app.modules.career_map import generate_career_map

st.set_page_config(page_title="AI Career Companion", layout="wide")
st.title("AI Career Companion")

sidebar_choice = st.sidebar.selectbox(
    "Choose a Module",
    ["Generate Docs", "Mock Interview", "Cheat Sheet", "Career Map"]
)

if sidebar_choice == "Generate Docs":
    st.header("Resume & Cover Letter Generator")
    uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    resume_details = None
    if uploaded_resume is not None:
        from app.modules.generate_doc.resume_parser import extract_resume_details_from_pdf
        resume_details = extract_resume_details_from_pdf(uploaded_resume)
        st.text_area("Extracted Resume Text", resume_details.get('raw_text', ''), height=200)

    jd = st.text_area("Paste Job Description", key='jd')
    generate_resume_clicked = st.button("Generate Resume")
    if generate_resume_clicked:
        resume = generate_resume(jd, resume_details)
        st.text_area("Generated Resume", resume, height=300)
        st.session_state['show_suggestions'] = True
        st.session_state['resume'] = resume
    # Show suggestions only after resume is generated
    if st.session_state.get('show_suggestions', False):
        st.subheader("Upgrade Suggestions")
        upgrade_projects = st.checkbox("Would you like to get suggestions to upgrade your projects?", key='upgrade_projects')
        upgrade_skills = st.checkbox("Would you like to get suggestions to upgrade your skills?", key='upgrade_skills')
        suggestions = None
        if (st.session_state.get('upgrade_projects') or st.session_state.get('upgrade_skills')) and resume_details:
            from app.modules.generate_doc import genai
            prompt = f"Given the following resume and job description, suggest improvements.\n\nResume:\n{resume_details.get('raw_text', '')}\n\nJob Description:\n{jd}"
            if st.session_state.get('upgrade_projects'):
                prompt += "\n\nSuggest 2-3 impactful projects to add or upgrade based on current experience and the job description."
            if st.session_state.get('upgrade_skills'):
                prompt += "\n\nSuggest 2-3 in-demand skills to learn or improve, relevant to the job description."
            prompt += "\n\nIf any important certifications are missing for this job, recommend them as well."
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            response = model.generate_content(prompt)
            suggestions = response.text if hasattr(response, 'text') else str(response)
            st.text_area("Upgrade Suggestions", suggestions, height=200)
            if suggestions:
                if st.button("Apply Suggestions to Resume"):
                    full_prompt = f"Rewrite my resume for this job: {jd}\n\nCurrent resume:\n{resume_details.get('raw_text', '')}\n\nApply these suggestions: {suggestions}\n\nAdd or update other sections (like summary, certifications, etc.) as needed for the job role.\n\nNote: The following projects, skills, and certifications are suggested for the user to pursue and learn. Add them to the resume, but it is the user's responsibility to actually learn or complete them."
                    improved_resume = model.generate_content(full_prompt)
                    improved_resume_text = improved_resume.text if hasattr(improved_resume, 'text') else str(improved_resume)
                    st.session_state['improved_resume_text'] = improved_resume_text
                    st.text_area("Improved Resume", improved_resume_text, height=300)
                    # Download button for improved resume
                    if hasattr(improved_resume, 'text'):
                        from io import BytesIO
                        import re
                        import docx
                        # Clean and format the resume for ATS (no stars, no bullet points, clear sections)
                        clean_text = re.sub(r'[★*•●▪️-]+', '', improved_resume.text)
                        clean_text = re.sub(r'\n+', '\n', clean_text)
                        # Create a DOCX document for professional formatting
                        doc = docx.Document()
                        doc.add_heading('Professional Resume', 0)
                        for para in clean_text.split('\n'):
                            if para.strip():
                                doc.add_paragraph(para.strip(), style='Normal')
                        buffer = BytesIO()
                        doc.save(buffer)
                        buffer.seek(0)
                        st.download_button(
                            label="Download ATS-Optimized Resume (DOCX)",
                            data=buffer,
                            file_name="ATS_Optimized_Resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
    if st.button("Generate Cover Letter"):
        # Use improved resume if available, else use the latest generated resume
        improved_resume_text = None
        if 'improved_resume_text' in st.session_state:
            improved_resume_text = st.session_state['improved_resume_text']
        elif 'resume' in st.session_state:
            improved_resume_text = st.session_state['resume']
        else:
            improved_resume_text = resume_details.get('raw_text', '') if resume_details else ''
        # Try to extract name and other details from resume
        import re
        name = ''
        # Simple name extraction: first line with 2+ capitalized words
        for line in improved_resume_text.split('\n'):
            if len(re.findall(r'[A-Z][a-z]+', line)) >= 2 and len(line.split()) <= 5:
                name = line.strip()
                break
        # Compose prompt for cover letter
        cover_letter_prompt = f"Write a professional cover letter for the following job description, using the following resume as context.\n\nJob Description:\n{jd}\n\nResume:\n{improved_resume_text}\n\nMy name is {name}. Use my name and any other relevant details from my resume in the cover letter."
        from app.modules.generate_doc import genai
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        cl_response = model.generate_content(cover_letter_prompt)
        cl = cl_response.text if hasattr(cl_response, 'text') else str(cl_response)
        st.text_area("Generated Cover Letter", cl, height=300)

elif sidebar_choice == "Mock Interview":
    st.header("Mock Algorithmic Interview")
    question = st.text_area("Describe your problem / paste code")
    if st.button("Start Interview"):
        feedback = run_mock_interview(question)
        st.text_area("Feedback & Hints", feedback, height=300)

elif sidebar_choice == "Cheat Sheet":
    st.header("Algorithm Cheat Sheet Generator")
    topic = st.text_input("Algorithm Topic (e.g. Dynamic Programming)")
    if st.button("Generate Cheat Sheet"):
        sheet = generate_cheat_sheet(topic)
        st.text_area("Cheat Sheet", sheet, height=400)

else:
    st.header("Career Path Explorer")
    profile = st.text_area("Tell us about your interests & skills")
    if st.button("Generate Career Map"):
        roadmap = generate_career_map(profile)
        st.text_area("Career Roadmap", roadmap, height=400)
