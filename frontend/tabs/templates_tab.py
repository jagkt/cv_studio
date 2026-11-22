import streamlit as st
from backend.storage import (
    get_active_cv_templates,
    get_active_letter_templates,
    update_cv_template,
    update_letter_template,
    reset_templates_to_default,
)


def render_templates_tab():
    st.subheader("Customize & Save Output Templates")
    st.write(
        "Modify the Markdown structures and evaluation rules used across **Analyze**, **Rewrite CV**, **Build New CV**, "
        "and **Letters / Statements**. Changes are saved locally in `data/user_profile.json`."
    )

    sub_cv, sub_letter = st.tabs(["CV Templates (Enterprise & Academic)", "Letter & Statement Templates"])

    with sub_cv:
        cv_templates = get_active_cv_templates()
        selected_track = st.selectbox("Select CV Track to Edit", options=list(cv_templates.keys()))
        cfg = cv_templates[selected_track]

        edited_focus = st.text_area(
            "Evaluation & ATS Analysis Criteria",
            value=cfg["analysis_focus"],
            height=90,
        )
        edited_structure = st.text_area(
            "Markdown Output Structure",
            value=cfg["structure"],
            height=340,
        )

        if st.button("Save CV Template", type="primary"):
            update_cv_template(selected_track, edited_focus, edited_structure)
            st.success(f"Saved custom template for **{selected_track}**!")

    with sub_letter:
        letter_templates = get_active_letter_templates()
        selected_doc = st.selectbox("Select Letter / Statement Template to Edit", options=list(letter_templates.keys()))
        doc_cfg = letter_templates[selected_doc]

        edited_doc_structure = st.text_area(
            "Document Markdown Structure",
            value=doc_cfg["structure"],
            height=340,
        )

        if st.button("Save Document Template", type="primary"):
            update_letter_template(selected_doc, edited_doc_structure)
            st.success(f"Saved custom template for **{selected_doc}**!")

    st.divider()
    if st.button("Reset All Templates to Factory Defaults"):
        reset_templates_to_default()
        st.warning("All templates have been restored to their default structures.")
        st.rerun()
