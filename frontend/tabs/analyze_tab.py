import streamlit as st
from backend.templates import CV_TEMPLATES
from backend.analysis import analyze_resume, extract_match_score


def render_analyze_tab(job_type: str, job_description: str):
    st.subheader(f"Compatibility Analysis ({job_type})")
    st.write(f"Evaluates your CV using **{job_type}** benchmarks against the target description.")

    with st.expander("View Active Evaluation Criteria & Target CV Template"):
        st.info(CV_TEMPLATES[job_type]["analysis_focus"])
        st.code(CV_TEMPLATES[job_type]["structure"], language="markdown")

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        run_analysis = st.button("Run Compatibility Analysis", type="primary", use_container_width=True)

    if run_analysis:
        if not st.session_state.get("full_resume"):
            st.error("Please upload your Resume / CV (PDF) in the sidebar first.")
        elif not job_description.strip():
            st.error("Please paste a Target Job Description / Call in the sidebar.")
        else:
            with st.spinner(f"Analyzing CV against {job_type} criteria..."):
                result = analyze_resume(st.session_state.full_resume, job_description, job_type)
                st.session_state.analysis = result
                st.session_state.match_score = extract_match_score(result)
                st.rerun()

    if "analysis" in st.session_state:
        score = st.session_state.get("match_score", 0)
        if 0 < score < 75:
            st.warning(
                f"Alignment score is **{score}%**. Use **2. Rewrite CV** or **3. New CV from History** "
                f"to automatically tailor your CV to the **{job_type}** template."
            )
        with st.container(border=True):
            st.markdown(st.session_state.analysis)
    else:
        st.info("Upload your PDF and paste the Job Description / Call in the sidebar, then click **Run Compatibility Analysis**.")
