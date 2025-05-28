



# AI Career Companion

AI Career Companion is a Streamlit-based application that helps users generate ATS-optimized resumes and cover letters, receive project and skill upgrade suggestions, and explore career paths using Google Gemini AI.

## Features
- **Resume & Cover Letter Generator:**
  - Upload your resume (PDF) and extract details automatically.
  - Generate a new resume tailored to a job description using Gemini AI.
  - Get AI-powered suggestions to upgrade your projects, skills, and certifications.
  - Apply suggestions and download a clean, ATS-friendly DOCX resume.
  - Generate a professional cover letter based on your improved resume and job description.
- **Mock Interview:**
  - Get feedback and hints on your coding or algorithmic questions.
- **Cheat Sheet Generator:**
  - Instantly generate algorithm cheat sheets for any topic.
- **Career Path Explorer:**
  - Get a personalized career roadmap based on your interests and skills.

## Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd AI-Career-Companion
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Add your Google API key and other settings to a `.env` file:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   DATABASE_URL=sqlite:///./app.db
   REDIS_URL=redis://localhost:6379
   ```

## Usage
Run the Streamlit app:
```sh
streamlit run streamlit_app.py
```
Open the provided local URL in your browser.

## Notes
- For resume PDF parsing, only text-based PDFs are supported (not scanned images).
- The app uses Google Gemini (Generative AI) for all AI-powered features.
- All generated resumes are formatted for high ATS scores (no stars, bullets, or non-ATS-friendly symbols).

## Project Structure
- `streamlit_app.py` - Main Streamlit app
- `app/modules/generate_doc/` - Resume, cover letter, and parsing logic
- `app/modules/mock_interview/` - Mock interview logic
- `app/modules/cheat_sheet/` - Cheat sheet generator
- `app/modules/career_map/` - Career path explorer
- `app/utils/` - Settings and utility functions

## License
MIT
