CV_TEMPLATES = {
    "Enterprise / Industry": {
        "description": "ATS-optimized corporate format emphasizing measurable impact, skills alignment, and concise 1–2 page structure.",
        "analysis_focus": (
            "Evaluate against corporate ATS standards: hard/soft skill keyword density, quantified business impact "
            "(revenue, latency, efficiency, scale), leadership, and role alignment."
        ),
        "structure": """
# [Full Name]
[City, Country] | [Phone] | [Email] | [LinkedIn / Portfolio / GitHub]

## Professional Summary
[3–4 lines positioning the candidate specifically for the target role, highlighting core domain expertise and measurable value.]

## Core Competencies & Technical Skills
- **[Category 1]:** [Relevant skills matching JD]
- **[Category 2]:** [Tools, frameworks, methodologies matching JD]

## Professional Experience
### [Job Title] — [Company Name] | [Start Date – End Date]
- [Action Verb] + [Task/Project] + [Quantifiable Result/Metric aligned to JD keywords].
- [Action Verb] + [Collaboration/Leadership/System impact].

## Key Projects (Optional)
- **[Project Name]:** [1–2 line summary highlighting tools used and outcome.]

## Education & Certifications
- **[Degree]** — [Institution] ([Year])
- **[Relevant Certifications]**
""",
    },
    "Academic / Research": {
        "description": "Scholarly CV format highlighting research agenda, publications, grants, teaching, and academic service.",
        "analysis_focus": (
            "Evaluate against academic hiring/admissions standards: research fit with department/PI, methodological rigor, "
            "publications/preprints, grants/funding, teaching/mentoring record, and scholarly impact."
        ),
        "structure": """
# [Full Name], [Degrees e.g., Ph.D. / M.Sc.]
[Department / Institution] | [Email] | [Google Scholar / ORCID / Website]

## Research Interests
[Concise 2–3 line statement of core research themes, methodologies, and domain focus aligned to the academic call.]

## Education
- **[Degree in Field]**, [University Name] ([Year])
  - *Thesis/Dissertation:* "[Title]" (Advisor: [Name])

## Academic & Research Appointments
### [Role, e.g., Postdoctoral Fellow / Graduate Researcher] — [Institution/Lab] | [Dates]
- [Research focus, methodologies, datasets, or experimental breakthroughs.]

## Publications & Preprints
- [Authors]. ([Year]). "[Paper Title]." *[Journal / Conference Name]*.

## Grants, Fellowships & Honors
- **[Award / Grant Name]**, [Funding Body] ([Year]) — [Role/Amount if applicable]

## Teaching & Mentorship Experience
- **[Course Title / Role]**, [Institution] ([Term/Year]) — [Brief summary of lecturing, curriculum design, or student supervision.]

## Academic Service & Referees
- [Peer review, workshop organization, or 'References available upon request.']
""",
    },
}

LETTER_TEMPLATES = {
    "Cover Letter (Enterprise / Job Application)": {
        "job_type": "Enterprise / Industry",
        "audience": "Hiring Manager & Recruitment Team",
        "structure": """
**[Candidate Name]**
[Email] | [Phone] | [LinkedIn/Location]

**Date:** [Current Date]
**To:** Hiring Team / [Hiring Manager Name], [Company Name]
**Subject:** Application for [Target Role]

Dear Hiring Manager,

**Opening Hook:** State the exact role applied for, express enthusiasm for [Company Name]'s mission/product, and present a strong 1-sentence value proposition.

**Core Alignment & Evidence (Body Paragraph 1):** Connect the candidate's strongest historical achievements and measurable outcomes directly to the top requirements in the Job Description.

**Technical/Domain Depth & Culture Fit (Body Paragraph 2):** Highlight specific tools, leadership, or problem-solving examples from their background that solve the team's pain points.

**Closing & Call to Action:** Reiterate enthusiasm for contributing to [Company Name] and request an interview.

Sincerely,
**[Candidate Name]**
""",
    },
    "Statement of Purpose (SOP — Graduate / PhD / Fellowship)": {
        "job_type": "Academic / Research",
        "audience": "Admissions Committee / Faculty Selection Panel",
        "structure": """
# Statement of Purpose: [Target Program / Fellowship / Position]

**1. Intellectual Hook & Research Goal:** Open with the specific research problem or intellectual question driving the candidate, and clearly state the program/position sought.

**2. Academic Foundation & Research Experience:** Synthesize prior research projects, methodologies mastered, theses, or publications from the candidate's history that prove readiness for rigorous inquiry.

**3. Alignment with Target Institution / Lab:** Explain specifically why this department, faculty, lab resources, or job call is the ideal environment for the candidate's proposed work.

**4. Future Trajectory & Impact:** Articulate short- and long-term scholarly/career goals following completion of the program or fellowship.
""",
    },
    "Motivation Letter (Scholarships / Labs / International Roles)": {
        "job_type": "Academic / Research",
        "audience": "Selection Committee / Program Coordinator",
        "structure": """
# Motivation Letter: [Target Opportunity / Program / Role]

**1. Introduction & Purpose:** Clearly state the program, scholarship, or role being applied for and the core motivation behind applying.

**2. Relevant Background & Track Record:** Highlight key academic, technical, or leadership milestones from the candidate's historical experience that demonstrate capability and resilience.

**3. Why This Program / Organization:** Connect the candidate's personal values and ambitions with the specific structure and mission of the target opportunity.

**4. Mutual Value & Closing:** Summarize how the candidate will actively contribute to the cohort/team and close professionally.
""",
    },
    "Research Statement (Faculty / Postdoc / R&D Positions)": {
        "job_type": "Academic / Research",
        "audience": "Faculty Search Committee / Principal Investigator / R&D Lead",
        "structure": """
# Research Statement: [Candidate Name]

## 1. Research Vision & Overview
[High-level summary of the candidate's core research program, overarching questions, and significance to the field.]

## 2. Past & Current Research Accomplishments
[Structured synthesis of prior empirical, theoretical, or engineering contributions drawn from the candidate's historical experience, citing methods and findings.]

## 3. Near-Term Research Agenda (1–3 Years)
[Concrete projects, methodologies, and deliverables aligned with the target position's focus areas.]

## 4. Long-Term Vision & Funding/Collaboration Potential
[Broader impact, interdisciplinary potential, and alignment with grant agencies or R&D priorities.]
""",
    },
}
