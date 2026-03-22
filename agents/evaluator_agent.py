from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from core import JobSearchState, EvaluationResult
import os


GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

def evaluator_agent(state: JobSearchState):
    print("Evaluator Agent: Scoring resume against job requirements...")
    
    resume_text = state.get("user_resume")
    must_haves = state.get("must_have_skills", [])
    nice_to_haves = state.get("nice_to_have_skills", [])
    
    if not resume_text or not must_haves:
        print("Evaluator Agent: Missing resume or job skills. Skipping evaluation.")
        return {
            "match_score": 0,
            "missing_keywords": ["Error: Missing input data"],
            "experience_gaps": []
        }
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
    structured_llm = llm.with_structured_output(EvaluationResult)
    
    prompt_template = PromptTemplate.from_template(
        "You are a strict, highly critical Applicant Tracking System (ATS) and Senior Technical Recruiter. "
        "Your job is to evaluate a candidate's resume against a list of required skills for a specific role.\n\n"
        "Do NOT hallucinate skills. If the resume does not explicitly state or strongly imply a skill, assume the candidate does not have it.\n\n"
        "Mandatory Skills Required: {must_haves}\n"
        "Bonus Skills Preferred: {nice_to_haves}\n\n"
        "Candidate Resume:\n{resume}\n\n"
        "Provide a match score (0-100), list the exact missing technical keywords, and identify any broader experience gaps."
    )
    
    formatted_prompt = prompt_template.format(
        must_haves=", ".join(must_haves),
        nice_to_haves=", ".join(nice_to_haves),
        resume=resume_text
    )
    
    result = structured_llm.invoke(formatted_prompt)
    
    print(f"Evaluator Agent: Resume scored a {result.match_score}/100.")
    if result.missing_keywords:
        print(f"Missing keywords identified: {len(result.missing_keywords)}")
    
    return {
        "match_score": result.match_score,
        "missing_keywords": result.missing_keywords,
        "experience_gaps": result.experience_gaps
    }
