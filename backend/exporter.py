import io
import re
from docx import Document
from docx.shared import Pt, Inches


def generate_docx_bytes(markdown_text: str) -> bytes:
    """Converts a Markdown CV or Letter into a clean, ATS-friendly .docx file (stripping post-'---' AI notes)."""
    clean_md = markdown_text.split("\n---")[0].strip()

    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)

    def add_formatted_runs(paragraph, text):
        parts = re.split(r"(\*\*.*?\*\*)", text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                run = paragraph.add_run(part[2:-2])
                run.bold = True
            else:
                paragraph.add_run(part)

    for raw_line in clean_md.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# "):
            p = doc.add_heading(line[2:].replace("**", ""), level=0)
            p.paragraph_format.space_after = Pt(4)
        elif line.startswith("## "):
            p = doc.add_heading(line[3:].replace("**", ""), level=1)
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
        elif line.startswith("### "):
            p = doc.add_heading(line[4:].replace("**", ""), level=2)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
        elif line.startswith(("- ", "* ")):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            add_formatted_runs(p, line[2:])
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            add_formatted_runs(p, line)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
