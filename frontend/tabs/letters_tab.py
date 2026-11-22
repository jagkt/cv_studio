import streamlit as st
from backend.templates import LETTER_TEMPLATES
from backend.doc_generator import generate_tailored_document
from frontend.ui_helpers import get_combined_candidate_context, render_download_bar


def render_letters_tab(job_description: str):
    st.subheader("Tailored Letters & Academic Statements")
    st.write(
        "Generate a **Cover Letter**, **Statement of Purpose (SOP)**, **Motivation Letter**, or **Research Statement** "
        "guided by predefined structural templates and grounded in your real experience."
    )

    doc_type = st.selectbox(
        "Select Document Type",
        options=list(LETTER_TEMPLATES.keys()),
    )

    doc_cfg = LETTER_TEMPLATES[doc_type]
    st.caption(f"**Target Audience:** {doc_cfg['audience']}  |  **Recommended Track:** {doc_cfg['job_type']}")

    with st.expander(f"View Predefined Template for {doc_type}"):
        st.code(doc_cfg["structure"], language="markdown")

    extra_notes = st.text_area(
        "Specific Points, Faculty Names, Lab/Company Hook, or Research Focus to Emphasize (Optional)",
        height=110,
        placeholder="e.g., Mention Prof. Jane Doe's work on distributed systems, or highlight my 3 years scaling Kubernetes clusters...",
    )

    col_doc, _ = st.columns([1, 2])
    with col_doc:
        short_label = doc_type.split(" (")[0]
        run_letter = st.button(f"Generate {short_label}", type="primary", use_container_width=True)

    if run_letter:
        candidate_context = get_combined_candidate_context()
        if not candidate_context.strip():
            st.error("Please upload your Resume/CV PDF in the sidebar or paste your career history in Tab 3 first.")
        elif not job_description.strip():
            st.error("Please paste the Target Job Description / Program Call in the sidebar.")
        else:
            with st.spinner(f"Drafting tailored {doc_type}..."):
                generated = generate_tailored_document(
                    doc_type=doc_type,
                    candidate_context=candidate_context,
                    job_description=job_description,
                    extra_instructions=extra_notes,
                )
                st.session_state.generated_letter = generated
                st.session_state.generated_letter_type = doc_type

    if "generated_letter" in st.session_state:
        st.markdown(f"### Preview: {st.session_state.get('generated_letter_type', doc_type)}")
        with st.container(border=True):
            st.markdown(st.session_state.generated_letter)

        st.markdown("#### Export Document")
        file_slug = (
            st.session_state.get("generated_letter_type", "document")
            .split(" (")[0]
            .lower()
            .replace(" ", "_")
        )
        render_download_bar(st.session_state.generated_letter, f"tailored_{file_slug}", "docgen")
