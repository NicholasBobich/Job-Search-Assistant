from typing import TypedDict, List, Optional

class JobSearchState(TypedDict):
    job_url: str
    user_resume: str
    raw_job_posting: Optional[str]
    
    # Extracted from the job posting
    must_have_skills: Optional[List[str]]
    nice_to_have_skills: Optional[List[str]]
    company_culture_tone: Optional[str]
    
    # Evaluator outputs
    match_score: Optional[int]
    missing_keywords: Optional[List[str]]
    experience_gaps: Optional[List[str]]
    
    # Writer outputs
    resume_tweaks: Optional[List[str]]
    drafted_cover_letter: Optional[str]
