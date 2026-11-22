import streamlit as st
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.vector_store import create_vector_store
from backend.cv_builder import build_new_cv_from_history
from backend.storage import load_user_data, save_master_history
from frontend.ui_helpers import render_download_bar


def render_new_cv_tab(job_type: str, job_description: str):
    st.subheader(f"Build Brand-New Tailored CV from Historical Experience ({job_type})")
    st.write(
        "Your career archive is saved locally on disk (`data/user_profile.json`) so you never lose it across sessions. "
        "The AI **extracts only the relevant items** required by the Job Description and builds a focused CV."
    )

    # Hydrate from local storage on initial load
    if "master_history_text" not in st.session_state:
        st.session_state.master_history_text = load_user_data().get("master_history", "")

    target_role = st.text_input(
        "Target Role / Position Title",
        placeholder="e.g., Senior Cloud Architect (Enterprise) OR Postdoctoral Fellow in Machine Learning (Academic)",
    )

    include_uploaded = st.checkbox(
        "Include text from uploaded PDF as part of my historical archive",
        value=bool(st.session_state.get("full_resume")),
        disabled=not bool(st.session_state.get("full_resume")),
    )

    master_history_input = st.text_area(
        "Complete Historical Experience Archive (Jobs, Research, Publications, Projects, Grants, Education)",
        value=st.session_state.master_history_text,
        height=240,
        placeholder="Paste all historical roles, publications, projects, tools, and education here...",
    )
    st.session_state.master_history_text = master_history_input

    col_build, col_save = st.columns([2, 1])
    with col_build:
        run_build_cv = st.button("Extract Relevant Experience & Build New CV", type="primary", use_container_width=True)
    with col_save:
        if st.button("Save Archive Locally", use_container_width=True):
            save_master_history(master_history_input)
            st.toast("Career archive saved locally to data/user_profile.json!", icon="✅")

    if run_build_cv:
        combined_parts = []
        if include_uploaded and st.session_state.get("full_resume"):
            combined_parts.append("=== UPLOADED PDF ===\n" + st.session_state.full_resume)
        if master_history_input.strip():
            combined_parts.append("=== HISTORICAL EXPERIENCE ARCHIVE ===\n" + master_history_input.strip())

        master_history = "\n\n".join(combined_parts)

        if not master_history.strip():
            st.error("Please upload a PDF or paste your historical experience above.")
        elif not job_description.strip():
            st.error("Please paste a Target Job Description / Call in the sidebar.")
        else:
            save_master_history(master_history_input)
            with st.spinner("Filtering relevant history and building your new CV..."):
                splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
                history_chunks = splitter.split_documents([Document(page_content=master_history)])
                st.session_state.vector_store = create_vector_store(history_chunks)

                new_cv = build_new_cv_from_history(
                    master_history=master_history,
                    job_description=job_description,
                    job_type=job_type,
                    target_role=target_role,
                )
                st.session_state.new_tailored_cv = new_cv

    if "new_tailored_cv" in st.session_state:
        st.success(f"Brand-new {job_type} CV built from your relevant historical experience!")
        with st.container(border=True):
            st.markdown(st.session_state.new_tailored_cv)

        st.markdown("#### Export Brand-New CV")
        slug = "enterprise" if "Enterprise" in job_type else "academic"
        render_download_bar(st.session_state.new_tailored_cv, f"tailored_new_{slug}_cv", "newcv")
