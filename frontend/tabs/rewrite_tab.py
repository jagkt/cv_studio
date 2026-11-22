import streamlit as st
from backend.templates import CV_TEMPLATES
from backend.cv_builder import rewrite_resume
from frontend.ui_helpers import render_download_bar


def render_rewrite_tab(job_type: str, job_description: str):
    st.subheader(f"Rewrite & Format Existing CV ({job_type} Template)")
    st.write("Reframes your existing CV to match the target description while strictly adhering to the selected template.")

    with st.expander("Preview Predefined Template Used for Rewriting"):
        st.code(CV_TEMPLATES[job_type]["structure"], language="markdown")

    col_rw, _ = st.columns([1, 2])
    with col_rw:
        run_rewrite = st.button(f"Rewrite CV ({job_type})", type="primary", use_container_width=True)

    if run_rewrite:
        if not st.session_state.get("full_resume"):
            st.error("Please upload your Resume / CV (PDF) in the sidebar first.")
        elif not job_description.strip():
            st.error("Please paste a Target Job Description / Call in the sidebar.")
        else:
            with st.spinner(f"Rewriting CV using {job_type} template..."):
                rewritten = rewrite_resume(
                    st.session_state.full_resume,
                    job_description,
                    job_type=job_type,
                    analysis_feedback=st.session_state.get("analysis", ""),
                )
                st.session_state.rewritten_resume = rewritten

    if "rewritten_resume" in st.session_state:
        view_clean, view_diff = st.tabs(["Formatted CV Preview", "Side-by-Side Comparison"])

        with view_clean:
            with st.container(border=True):
                st.markdown(st.session_state.rewritten_resume)

        with view_diff:
            c_left, c_right = st.columns(2)
            with c_left:
                st.markdown("**Original Extracted Text**")
                st.text_area(
                    "Original CV",
                    value=st.session_state.full_resume,
                    height=480,
                    label_visibility="collapsed",
                )
            with c_right:
                st.markdown(f"**Rewritten ({job_type})**")
                with st.container(height=480, border=True):
                    st.markdown(st.session_state.rewritten_resume)

        st.markdown("#### Export Rewritten CV")
        slug = "enterprise" if "Enterprise" in job_type else "academic"
        render_download_bar(st.session_state.rewritten_resume, f"rewritten_{slug}_cv", "rw")
