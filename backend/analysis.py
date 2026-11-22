import re
from langchain_core.prompts import PromptTemplate
from backend.llm import llm
from backend.templates import CV_TEMPLATES


def extract_match_score(analysis_text: str) -> int:
    """Extracts the numeric match percentage from the LLM analysis output."""
    match = re.search(r"Match Percentage\*?\*?:\s*(\d{1,3})\s*%", analysis_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0


def analyze_resume(full_resume:str, job_description: str, job_type: str= "Enterprise / Industry") -> str:
    """Evaluates how well an existing resume aligns with the target JD using Enterprise or Academic criteria."""
    template_cfg = CV_TEMPLATES.get(job_type, CV_TEMPLATES["Enterprise / Industry"])
    
    # template = template_cfg["template"]
    template = """
    You are an expert recruiter and selection committee evaluator specializing in **{job_type}** applications.
    Evaluation Criteria: {analysis_focus}

    Compare the candidate's resume/CV against the target Job Description / Call. Keep your response crisp and under 450 words.

    Use this exact Markdown structure:

    ### Overview ({job_type} Track)
    - **Match Percentage**: [Number]%
    - **Matched Qualifications & Keywords**: [Comma-separated list of matching skills/credentials]
    - **Missing Keywords / Gaps**: [Comma-separated list of missing JD requirements]

    ### Detailed Breakdown
    1. **Strengths & Alignment**: Why the candidate fits well for this {job_type} role.
    2. **Critical Gaps**: Key skills, publications, tools, or credentials missing from the CV.
    3. **Actionable Recommendations**: 2–3 concrete steps to improve match score.

    Resume / CV:
    {resume}

    Target Job Description / Call:
    {job_description}

    Analysis:
    """
    
    prompt = PromptTemplate(
        input_variables=["job_type", "analysis_focus", "resume", "job_description"],
        template=template,
    )
    chain = prompt | llm
    response = chain.invoke({
        "job_type": job_type,
        "analysis_focus": template_cfg["analysis_focus"],
        "resume": full_resume,
        "job_description": job_description
    })
    
    return response.content
    
    