# Job Search Assistant (Agentic AI Project)

Multi-agent AI pipeline built with **LangGraph** and **LangChain** that scrapes job postings, extracts requirements, evaluates the user's resume, and dynamically drafts cover letters and resume suggestions.

## Architecture

This project demonstrates a production-grade approach to Agentic AI by moving away from monolithic LLM prompts and instead utilizing a **StateGraph architecture**. 

The application is broken into four different agents that pass structured data through a shared state machine:

1. **Scraper Agent (Data Ingestion):** Scrapes the target job posting URL (and optionally the company's "About Us" page) and cleans the raw HTML into readable text.
2. **Extractor Agent (Structured Parsing):** Utilizes structured output to parse the raw text into strict JSON arrays of mandatory skills, preferred skills, and company culture.
3. **Evaluator Agent (Reasoning & Scoring):** Acts as an Applicant Tracking System (ATS). It compares the extracted requirements against the user's resume to generate a match score and explicitly identify missing technical keywords.
4. **Writer Agent (Generation):** Synthesizes the company culture, identified experience gaps, and the user's resume to draft a cover letter and resume bullet points.

## Tech Stack
* **Language:** Python 3.13.12
* **Orchestration:** LangGraph
* **LLM Integration:** LangChain, Google Gemini API
* **Data Validation:** Pydantic
* **Web Scraping:** BeautifulSoup4

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/autonomous-job-assistant.git](https://github.com/yourusername/autonomous-job-assistant.git)
   cd autonomous-job-assistant
2. **Create a Virtual Environment and Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate # Mac/Linux
   venv\Scripts\Activate.ps1 # Windows
   pip install -r requirements.txt
3. **Set Environment Variables**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"

## Run the App
```bash
python main.py \
  --job "[https://careers.company.com/job/123](https://careers.company.com/job/123)" \
  --resume "./my_resume.pdf" \
  --about "[https://company.com/about](https://company.com/about)" # Optional