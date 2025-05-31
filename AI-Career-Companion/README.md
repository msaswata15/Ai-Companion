# AI Career Companion

##Deployed Website https://ai-companio.streamlit.app/

## Overview
AI Career Companion is a modern, all-in-one Streamlit application designed to help job seekers accelerate their job search and application process using AI. The app provides:
- Automated job hunting and matching
- Tailored resume and cover letter generation
- Cheat sheet creation for technical interviews
- Voice-based mock interview practice (with Proctoring)

All features are seamlessly integrated for a professional, user-friendly experience.

---

## Features

### 🏠 Home (Full Workflow)
- Upload your resume (PDF) and a job description (JD)
- One-click: "Run Full AI Career Workflow" runs all modules in sequence:
  1. **Automated Job Hunter**: Finds relevant jobs and displays matches
  2. **Tailored Resume**: Generates a resume optimized for the job
  3. **Cover Letter**: Creates a custom cover letter
  4. **Cheat Sheet**: Auto-generates a study guide of key topics
  5. **Mock Interview**: Prepares you with AI-generated interview questions (viva only)
- Resume and JD uploads are shared across all features

### 🤖 Automated Job Hunter
- Find jobs by keywords, location, and source (Remotive, Adzuna)
- See job matches, tailored resume, and cover letter for each job
- Application status feedback (demo)

### 📄 Resume/Cover Letter
- Upload resume and JD, or use shared uploads from Home
- Generate a tailored resume and cover letter
- Download results as DOCX
- Get AI-powered suggestions for projects, skills, and certifications

### 📚 Cheat Sheet Generator
- Auto-detects topics from your resume and JD
- Generates concise cheat sheets for each topic
- Option to generate by custom topic

### 🎤 Mock Interview (with Proctor Mode)
- Upload resume and JD, or use shared uploads
- Viva (non-coding) and coding questions are supported
- **Coding Challenge:**
  - Only Python coding questions are given (DSA-focused)
  - One random coding question per session (persisted)
  - User code and hidden test case results persist after each run
  - Hidden test cases are checked and detailed error messages (with line numbers) are shown for failures
  - Robust session state management for code, results, and question
- **Proctor Mode:**
  - Webcam photo capture every 30 seconds
  - Tab switch/minimize detection and logging
  - Exam auto-termination after excessive tab switches
  - Download all proctoring data as a ZIP file
- Sequential question flow: one question at a time, with live audio recording and feedback (for viva)
- Live timers for each section
- After all questions, a holistic report is generated (strengths, improvements, resume-JD fit)
- Download the full report; session resets automatically for a new interview

---

## UI/UX Highlights
- Modern, modular Streamlit UI with custom CSS
- Sidebar navigation with clear highlighting
- Always-visible, context-aware workflow button on Home
- All uploads are session-shared for seamless experience
- HTML tags are stripped from job descriptions for clean display
- Audio files are ignored by git and stored in `temp_audio/`
- Proctoring session data is stored in `proctor_session_data/`


  ![image](https://github.com/user-attachments/assets/096cfe8b-8ef6-4aff-a3f2-005c38131cea)

  ![image](https://github.com/user-attachments/assets/87fa11bf-cc5d-4267-b124-9f29eeb8d0a5)


## Proctor Mode (Mock Interview)
- Webcam photo capture every 30 seconds
- Tab switch/minimize detection and logging
- Exam auto-termination after excessive tab switches
- Download all proctoring data as a ZIP file
- Coding challenge is handled separately from voice (viva) questions

---

## Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd AI-Career-Companion
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```sh
   streamlit run streamlit_app.py
   ```

---

## Folder Structure
- `streamlit_app.py` — Main Streamlit app
- `app/modules/` — Modular feature logic (resume, job hunter, interview, cheat sheet, proctoring, etc.)
- `app/utils/` — Utility functions (job fetching, etc.)
- `temp_audio/` — Temporary audio files (ignored by git)
- `proctor_session_data/` — Proctoring session data (ignored by git)
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation

---

## License
This project is licensed under the MIT License.

---

## Acknowledgements
- Built with [Streamlit](https://streamlit.io/)
- Uses Google Gemini API for AI content generation
- Job data from Remotive and Adzuna APIs

---

## Contact
For questions or contributions, please open an issue or pull request on GitHub.
