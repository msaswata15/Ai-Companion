# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

---

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

---

## AI Career Companion

A single web application that helps students:

- **Generate** tailored resumes & cover letters from any job/scholarship posting
- **Coach** them through live mock algorithmic interviews—with hints, code evaluation & feedback
- **Build** personalized algorithm cheat-sheets on demand

| **Criterion**                   | **Feature**                                                                                                                                           | **Why it Scores**                                                                                |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Innovation & Creativity (25%)   | End-to-end “Career Companion” flow, unique UX tying resume → interview → cheat sheet                                                                  | It’s more than a bot—it’s a full funnel.                                                         |
| Technical Complexity (25%)      | • GPT-4/OpenAI embeddings for JD parsing & answer grading<br>• Real-time code exec & sandboxing<br>• Dynamic cheat-sheet generation via prompt chains | Hard AI/ML plumbing + secure code evaluation + prompt orchestration.                             |
| Functionality & Usability (20%) | • Intuitive React (JS) UI wizard<br>• Spring Boot/Node.js API layer<br>• SQL for user data & analytics                                                | A polished, end-to-end Web app that actually “works” with user accounts, persistence, analytics. |
| Presentation & Demo (15%)       | • 3–5 min video flows through each module in sequence<br>• Live “generate” & “mock interview” demo                                                    | Clear narrative: “Here’s my cover letter → here’s me interviewing → here’s my cheat sheet.”      |
| GitHub Tools & Workflows (15%)  | • Copilot-driven coding (docs & screenshots)<br>• CI/CD via GitHub Actions to deploy to Vercel/Heroku<br>• Automated tests & lint checks              | Demonstrate real-world DevOps maturity and Copilot productivity.                                 |

---

Feel free to integrate this directly into your **README.md**, **slides.md**, or any presentation material. Let me know if you’d like additional sections—API overview, tech stack summary, or wiring up the demo video script next!
