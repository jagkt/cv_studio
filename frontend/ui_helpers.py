import streamlit as st
from backend.exporter import generate_docx_bytes

def inject_modern_css():
    st.markdown(
       """
        <style>
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stMetric"] {
            background-color: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.2);
            padding: 0.9rem 1.15rem;
            border-radius: 12px;
        }
        .hero-banner {
            padding: 1.2rem 1.5rem;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.14), rgba(16, 185, 129, 0.10));
            border: 1px solid rgba(59, 130, 246, 0.28);
            margin-bottom: 1.1rem;
        }
        .hero-banner h2 {
            margin: 0 0 0.25rem 0;
            font-size: 1.55rem;
        }
        .hero-banner p {
            margin: 0;
            opacity: 0.88;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    

def render_download_bar(markdown_content: str, base_filename: str, key_prefix:str):
    """Renders aligned Word (.docx) and Markdown (.md) download buttons."""
    docx_bytes = generate_docx_bytes(markdown_content)
    col1, col2 = st.column(2)
    
    with col1:
        st.download_button(
            label="Download Word Document (.docx)",
            data=docx_bytes,
            file_name=f"{base_filename}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            use_container_width=True,
            key=f"{key_prefix}_docx", 
        )
    
    with col2:
        st.download_button(
            label="Download Markdown (.md)",
            data=markdown_content,
            file_name=f"{base_filename}.md",
            mime="text/markdown",
            use_container_width=True,
            key=f"{key_prefix}_md", 
        )


def get_combined_candidate_context() -> str:
    """Combines uploaded PDF text with any master career history pasted by the user."""
    parts = []
    
    if st.session_state.get("full_resume"):
        parts.append("=== UPLOADED RESUME / CV ===\n" + st.session_state.full_resume)
    
    if st.session_state.get("master_history_text", "").strip():
        parts.append("=== HISTORICAL EXPERIENCE & PROJECTS ===\n" + st.session_state.master_history_text.strip())
    
    return "\n\n".join(parts)     