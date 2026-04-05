from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from core import JobSearchState, ExtractedJobDetails


def extractor_agent(state: JobSearchState):
    
    print("Extractor Agent: Gathering job requirements...")
    
    raw_job_posting = state.get("raw_job_posting")
    raw_about_us = state.get("raw_about_us")
    
    # If the scraper agent failed, pass empty data forward
    if not raw_job_posting or "Error" in raw_job_posting:
        print("Extractor Agent: No valid text found. Skipping extraction.")
        return {
            "must_have_skills": [], 
            "nice_to_have_skills": [], 
            "company_culture_tone": "Unknown"
        }
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    structured_llm = llm.with_structured_output(ExtractedJobDetails)
    
    prompt_template = PromptTemplate.from_template(
        "You are an expert technical recruiter. Analyze the following job posting "
        "and extract the required skills as well as any bonus/preferred skills or 'nice-to-haves'.\n\n"
        "To determine the 'company_culture_tone', use both the Job Posting and the Company About Page (if provided).\n\n"
        "Job Posting:\n{job_text}\n\n"
        "Company About Page:\n{about_text}"
    )
    
    formatted_prompt = prompt_template.format(
        job_text=raw_job_posting,
        about_text=raw_about_us if raw_about_us else "Not provided. Infer tone solely from job posting."
    )
    
    result = structured_llm.invoke(formatted_prompt)

    print("Extractor Agent: Requirements extracted successfully!")
    
    return {
        "must_have_skills": result.must_have_skills,
        "nice_to_have_skills": result.nice_to_have_skills,
        "company_culture_tone": result.company_culture_tone
    }
