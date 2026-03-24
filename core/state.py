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

class EvaluationResult(BaseModel):
    match_score: int = Field(
        description="A score from 0 to 100 representing how well the resume matches the job requirements."
    )
    missing_keywords: List[str] = Field(
        description="Specific technical terms, tools, or frameworks mentioned in the job posting that are completely missing from the resume."
    )
    experience_gaps: List[str] = Field(
        description="Broader conceptual gaps. For example, if the job requires 'leading a team' but the resume only shows individual work."
    )

class ApplicationMaterials(BaseModel):
    drafted_cover_letter: str = Field(
        description="A custom cover letter drafted for the specific job, matching the company's culture tone."
    )
    resume_tweaks: List[str] = Field(
        description="A list of 3-5 specific, rewritten resume bullet points that incorporate the missing keywords and address the experience gaps identified by the evaluator."
    )
