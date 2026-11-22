# Contributing to AI Career & Academic Document Studio

Thank you for your interest in contributing! Whether you are fixing a bug, adding new Enterprise/Academic templates, improving ATS scoring, or enhancing the UI, your contributions are welcome.

---

## Development Setup

1. **Fork & Clone the Repository**
   ```bash
   git clone https://github.com<your-username>/cv_studio.git
   cd cv_studio
   ```

2. **Create a Virtual Environment & Install Dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the project root (never commit `.env` or `data/user_profile.json`):
   ```env
   GROQ_API_KEY="your-groq-api-key"
   GROQ_MODEL="openai/gpt-oss-20b"
   ```

4. **Run Locally**
   ```bash
   streamlit run app.py
   ```

---

## Project Architecture Guidelines

Please keep contributions modular and respect the separation of concerns:

- **`backend/llm.py`**: Shared LLM initialization and model configuration.
- **`backend/templates.py`**: Default Enterprise and Academic CV/Letter templates.
- **`backend/storage.py`**: Local JSON persistence for user profiles and custom templates.
- **`backend/analysis.py`**: Resume-to-JD compatibility analysis and match score parsing.
- **`backend/cv_builder.py`**: CV rewriting and historical experience extraction logic.
- **`backend/doc_generator.py`**: Cover letter, SOP, motivation letter, and research statement generation.
- **`backend/exporters.py`**: Document export engines (`.docx`, `.md`, etc.).
- **`frontend/tabs/`**: Individual Streamlit UI modules for each workspace tab.

---

## Branching & Pull Request Workflow

1. Create a descriptive branch from `main`:
   ```bash
   git checkout -b feat/add-teaching-statement-template
   # or
   git checkout -b fix/docx-bullet-formatting
   ```
2. Keep commits focused and atomic with clear commit messages (e.g., `feat: add teaching statement template`, `fix: handle bold headers in docx exporter`).
3. Ensure no personal data (`data/`, `.env`, sample personal CVs) is staged before pushing.
4. Open a **Pull Request** describing:
   - What problem your change solves or what feature it adds.
   - Any new environment variables or dependencies introduced.
   - Screenshots if you modified the Streamlit frontend UI.

---

## Ideas for Contributions

- Additional academic templates (e.g., Teaching Statement, Diversity Statement, Grant Abstract).
- PDF export support alongside `.docx` and `.md`.
- Multi-profile switching in local storage.
- Automated unit tests for `extract_match_score` and `generate_docx_bytes`.

---

## Code of Conduct

Be respectful, constructive, and collaborative in all issues, reviews, and discussions.
