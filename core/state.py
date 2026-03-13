from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

class JobSearchState(TypedDict):
    job_url: str
    about_us_url: Optional[str]
    user_resume: str
    
    raw_job_posting: Optional[str]
    raw_about_us: Optional[str]  # New storage for the scraped page
    
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

class ExtractedJobDetails(BaseModel):
    must_have_skills: List[str] = Field(
        description="Skills and experience required for the role."
    )
    nice_to_have_skills: List[str] = Field(
        description="Bonus/preferred skills, or 'nice to have' experience."
    )
    company_culture_tone: str = Field(
        description="A short summary describing the company culture based on the job description."
    )
