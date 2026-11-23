from langchain_core.prompts import PromptTemplate
from backend.llm import llm
# from backend.templates import CV_TEMPLATES
from backend.storage import get_active_cv_templates



def rewrite_resume(
    full_resume: str,
    job_description: str,
    job_type: str = "Enterprise / Industry",
    analysis_feedback: str = "",
) -> str:
    """Rewrites an existing resume/CV using the predefined Enterprise or Academic template."""
    # template_cfg = CV_TEMPLATES.get(job_type, CV_TEMPLATES["Enterprise / Industry"])
    cv_templates = get_active_cv_templates()
    template_cfg = cv_templates.get(job_type, cv_templates["Enterprise / Industry"])
    
    template = """
    You are an executive resume and academic CV writer.
    Rewrite and optimize the candidate's existing resume so it aligns strongly with the target Job Description / Call under the **{job_type}** track.

    STRICT RULES:
    1. NEVER fabricate job titles, institutions, publications, dates, degrees, or fake metrics.
    2. Reframe existing accomplishments using strong action verbs and exact terminology from the Job Description where truthful.
    3. Follow this exact Markdown template structure (omit sections only if the candidate has zero relevant data for them):
    {cv_structure}
    4. Keep the entire CV under 650 words.
    5. At the very end after a `---` line, add 3 short bullets under `### Key Improvements Made`.

    Existing Resume:
    {resume}

    Target Job Description / Call:
    {job_description}

    Gap Analysis Notes:
    {analysis}

    Tailored CV:
    """
    
    prompt = PromptTemplate(
        input_variables=["job_type", "cv_structure", "resume", "job_description", "analysis"],
        template=template,
    )
    chain = prompt | llm
    response = chain.invoke({
        "job_type": job_type,
        "cv_structure": template_cfg["structure"],
        "resume": full_resume,
        "job_description": job_description,
        "analysis": analysis_feedback or "Optimize for maximum alignment with the target description.",
    })  
    
    return response.content
    
    

def build_new_cv_from_history(
    master_history: str,
    job_description: str,
    job_type: str = "Enterprise / Industry",
    target_role: str = "",
) -> str:
    """Extracts ONLY the relevant experience from full career history to build a brand-new CV matching the selected template."""
    # template_cfg = CV_TEMPLATES.get(job_type, CV_TEMPLATES["Enterprise / Industry"])
    cv_templates = get_active_cv_templates()
    template_cfg = cv_templates.get(job_type, cv_templates["Enterprise / Industry"])


    template = """
    You are a senior career architect and CV writer specializing in **{job_type}** applications.
    The candidate has provided their complete, unfiltered career history (past jobs, research, projects, publications, skills, and education).
    Your job is to SELECT ONLY the relevant experience, projects, publications, and skills needed for the Target Job Description, omit irrelevant noise, and write a brand-new CV from scratch.

    STRICT RULES:
    1. Extract ONLY roles, research, achievements, and skills directly relevant or transferable to the Job Description. Drop unrelated filler.
    2. NEVER invent facts, employers, papers, certifications, or metrics not supported by the master history.
    3. Position the candidate specifically for: {target_role}.
    4. Strictly follow this predefined **{job_type}** Markdown template:
    {cv_structure}
    5. Keep the entire CV under 650 words.
    6. At the very end after a `---` line, list `### Selection Rationale` (3 short bullets explaining what was prioritized and what irrelevant history was omitted).

    Candidate's Complete Historical Experience:
    {master_history}

    Target Job Description / Call:
    {job_description}

    New Tailored CV:
    """
    prompt = PromptTemplate(
        input_variables=["job_type", "target_role", "cv_structure", "master_history", "job_description"],
        template=template,
    )
    chain = prompt | llm
    response = chain.invoke({
        "job_type": job_type,
        "target_role": target_role or "the target position",
        "cv_structure": template_cfg["structure"],
        "master_history": master_history,
        "job_description": job_description,
    })
    
    return response.content
    