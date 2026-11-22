from langchain_core.prompts import PromptTemplate
from backend.llm import llm
from backend.templates import LETTER_TEMPLATES


def generate_tailored_document(
    doc_type: str,
    candidate_context: str,
    job_description: str,
    extra_instructions: str = "",
) -> str:
    """Generates a tailored Cover Letter, SOP, Motivation Letter, or Research Statement using predefined templates."""
    doc_cfg = LETTER_TEMPLATES[doc_type] 
    
    template = """
    You are an elite academic and executive communications writer.
    Write a compelling, personalized **{doc_type}** addressed to **{audience}** based strictly on the candidate's real background and the target description.

    STRICT RULES:
    1. NEVER fabricate degrees, employers, publications, awards, or experiences not found in the candidate's context.
    2. Weave concrete examples, skills, and achievements from the candidate's history directly into the narrative to address the target requirements.
    3. Follow this predefined Markdown template structure faithfully:
    {doc_structure}
    4. Keep the document focused, persuasive, and under 600 words.
    5. At the very end after a `---` line, add 3 short bullets under `### Alignment Highlights` summarizing how the letter targets the prompt.

    Candidate Background & Historical Experience:
    {candidate_context}

    Target Job Description / Program Call:
    {job_description}

    Additional Candidate Notes / Specific Points to Emphasize:
    {extra_instructions}

    Generated {doc_type}:
    """
    
    prompt = PromptTemplate(
        input_variables=["doc_type", "audience", "doc_structure", "candidate_context", "job_description", "extra_instructions"],
        template=template,
    )
    chain = prompt | llm
    
    response = chain.invoke({
        "doc_type": doc_type,
        "audience": doc_cfg["audience"],
        "doc_structure": doc_cfg["structure"],
        "candidate_context": candidate_context,
        "job_description": job_description,
        "extra_instructions": extra_instructions or "None provided.",
    })
    
    return response.content

    