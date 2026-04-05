from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from pypdf import PdfReader
import os
from graph import workflow_app


st.set_page_config(page_title="Job Search Assistant", page_icon="🤖", layout="wide")
st.title("Job Search Assistant")
st.write("Upload your resume and paste a job URL. The AI agents will scrape the posting, evaluate your fit, and draft a tailored cover letter.")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password", help="Get this from Google AI Studio")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    st.markdown("---")
    st.write("Built with **LangGraph**, **LangChain**, and **Streamlit**.")

col1, col2 = st.columns(2)

with col1:
    job_url = st.text_input("🔗 Job Posting URL", placeholder="https://careers.company.com/job/123")
    about_url = st.text_input("🏢 Company 'About Us' URL (Optional)", placeholder="https://company.com/about")

with col2:
    uploaded_file = st.file_uploader("📄 Upload your base resume", type=["pdf", "txt", "md"])

if st.button("🚀 Analyze & Generate", use_container_width=True):
    if not os.environ.get("GOOGLE_API_KEY"):
        st.error("Please enter your Google API Key in the sidebar.")
        st.stop()
        
    if not job_url or not uploaded_file:
        st.warning("Please provide both a Job URL and a Resume.")
        st.stop()

    resume_text = ""
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                resume_text += page.extract_text() + "\n"
        else:
            resume_text = uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading resume file: {e}")
        st.stop()

    initial_state = {
        "job_url": job_url,
        "about_us_url": about_url if about_url else None,
        "user_resume": resume_text,
    }

    with st.spinner("🕵️‍♂️ Agents are scraping, evaluating, and writing... This usually takes 15-30 seconds."):
        try:
            final_state = workflow_app.invoke(initial_state)
        except Exception as e:
            st.error(f"An error occurred during agent execution: {e}")
            st.stop()

    st.success("Analysis Complete!")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Evaluation Score", "📝 Resume Tweaks", "✉️ Cover Letter"])
    
    with tab1:
        st.subheader("ATS Match Score")
        score = final_state.get("match_score", 0)
        st.progress(score / 100.0, text=f"{score}/100 Match")
        
        missing_keywords = final_state.get("missing_keywords", [])
        if missing_keywords:
            st.warning("**Critical Missing Keywords:**\n" + ", ".join(missing_keywords))
        else:
            st.success("No critical keywords missing!")
            
    with tab2:
        st.subheader("Suggested Resume Additions")
        for tweak in final_state.get("resume_tweaks", []):
            st.info(tweak)
            
    with tab3:
        st.subheader("Drafted Cover Letter")
        st.text_area("Copy your cover letter here:", final_state.get("drafted_cover_letter", ""), height=400)
