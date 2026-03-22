from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from core import JobSearchState, ApplicationMaterials
import os


GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

def writer_agent(state: JobSearchState):

    print("Writer Agent: Drafting custom application materials...")
    
    resume_text = state.get("user_resume")
    tone = state.get("company_culture_tone", "Professional and standard")
    missing_keywords = state.get("missing_keywords", [])
    experience_gaps = state.get("experience_gaps", [])
    
    if not resume_text:
        return { 
            "drafted_cover_letter": "Error: No resume provided.", 
            "resume_tweaks": []
        }

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    structured_llm = llm.with_structured_output(ApplicationMaterials)
    
    prompt_template = PromptTemplate.from_template(
        "You are an expert career coach and writer. Your goal is to help a candidate land a job "
        "by addressing specific gaps in their resume and writing a compelling cover letter.\n\n"
        "Company Culture & Tone: {tone}\n"
        "Missing Technical Keywords: {keywords}\n"
        "Identified Experience Gaps: {gaps}\n\n"
        "Candidate's Current Resume:\n{resume}\n\n"
        "Task 1: Write a concise, engaging cover letter that matches the company's tone. Do not just summarize the resume; tell a story that bridges the candidate's background with the job.\n"
        "Task 2: Write 3 to 5 highly specific resume bullet points the candidate could add to their resume to address the missing keywords and gaps (assuming they actually have the proper skills but failed to highlight them properly)."
    )
    
    formatted_prompt = prompt_template.format(
        tone=tone,
        keywords=", ".join(missing_keywords) if missing_keywords else "None",
        gaps=", ".join(experience_gaps) if experience_gaps else "None",
        resume=resume_text
    )
    
    result = structured_llm.invoke(formatted_prompt)
    
    print("Writer Agent: Application materials drafted successfully!")
    
    return {
        "drafted_cover_letter": result.drafted_cover_letter,
        "resume_tweaks": result.resume_tweaks
    }
