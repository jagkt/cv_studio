import os
import shutil
import streamlit as st

from backend.pdf_ingestion import load_split_pdf
from backend.vector_store import create_vector_store
from backend.templates import CV_TEMPLATES
from frontend.ui_helpers import inject_modern_css
from frontend.tabs.analyze_tab import render_analyze_tab
from frontend.tabs.rewrite_tab import render_rewrite_tab
from frontend.tabs.new_cv_tab import render_new_cv_tab
from frontend.tabs.letters_tab import render_letters_tab
from frontend.chat_interface import render_chat_interface
from frontend.tabs.templates_tab import render_templates_tab


def render_sidebar():
    with st.sidebar:
        if os.path.exists("cv-studio-icon.svg"):
            st.image("cv-studio-icon.svg", width=90)

        st.header("1. Application Track")
        job_type = st.radio(
            "Select Target Track",
            options=list(CV_TEMPLATES.keys()),
            help="Switches evaluation criteria and output templates between Corporate/Industry and Academic/Research formats.",
        )
        st.session_state.job_type = job_type
        st.caption(CV_TEMPLATES[job_type]["description"])

        st.divider()
        st.header("2. Documents & Target Role")

        resume_file = st.file_uploader(
            "Upload Current Resume / CV (PDF)",
            type="pdf",
            help="Upload your existing resume or multi-page academic CV.",
        )

        if resume_file and st.session_state.get("uploaded_filename") != resume_file.name:
            with st.spinner("Indexing uploaded PDF..."):
                temp_dir = "temp"
                os.makedirs(temp_dir, exist_ok=True)
                resume_file_path = os.path.join(temp_dir, resume_file.name)

                with open(resume_file_path, "wb") as f:
                    f.write(resume_file.getbuffer())

                resume_docs, resume_chunks = load_split_pdf(resume_file_path)
                st.session_state.vector_store = create_vector_store(resume_chunks)
                st.session_state.full_resume = "\n".join([doc.page_content for doc in resume_docs])
                st.session_state.uploaded_filename = resume_file.name

                for k in ["analysis", "match_score", "rewritten_resume", "new_tailored_cv", "generated_letter"]:
                    st.session_state.pop(k, None)

                shutil.rmtree(temp_dir)
            st.success(f"Loaded: {resume_file.name}")

        job_description = st.text_area(
            "Target Job Description / Program Call",
            value=st.session_state.get("job_description", ""),
            height=230,
            placeholder="Paste the Job Description, Fellowship Call, or Academic Position details here...",
        )
        st.session_state.job_description = job_description

        if st.session_state.get("full_resume"):
            st.caption(f"PDF indexed ({len(st.session_state.full_resume)} chars)")

    return job_type, job_description


def render_main_app():
    inject_modern_css()
    job_type, job_description = render_sidebar()

    track_badge = "Enterprise / Industry Track" if "Enterprise" in job_type else "🎓 Academic / Research Track"
    st.markdown(
        f"""
        <div class="hero-banner">
            <h2>AI Career & Academic Document Studio</h2>
            <p>Active Mode: <strong>{track_badge}</strong> — Analyze fit, rewrite CVs, extract relevant career history, and draft tailored letters using structured templates.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "analysis" in st.session_state:
        score = st.session_state.get("match_score", 0)
        status_label = (
            "Strong Match" if score >= 75 else "Moderate Match — Rewrite Suggested" if score >= 50 else "Low Match — Tailoring Needed"
        )
        m1, m2, m3 = st.columns(3)
        m1.metric("Alignment Score", f"{score}%")
        m2.metric("Readiness Status", status_label)
        m3.metric("Selected Track", track_badge)

    tab_analyze, tab_rewrite, tab_new_cv, tab_letters, tab_chat, tab_templates = st.tabs([
        "1. Analyze",
        "2. Rewrite CV",
        "3. New CV from History",
        "4. Cover Letter / SOP / Statements",
        "5. Career AI Chat",
        "6. Templates",
    ])

    with tab_analyze:
        render_analyze_tab(job_type, job_description)

    with tab_rewrite:
        render_rewrite_tab(job_type, job_description)

    with tab_new_cv:
        render_new_cv_tab(job_type, job_description)

    with tab_letters:
        render_letters_tab(job_description)

    with tab_chat:
        render_chat_interface()
    
    with tab_templates:
        render_templates_tab()
