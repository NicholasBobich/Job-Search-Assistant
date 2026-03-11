from core import JobSearchState
import requests
from bs4 import BeautifulSoup


def scraper_agent(state: JobSearchState):
    job_url = state.get("job_url")
    if not job_url:
        return {"raw_job_posting": "Error: No job URL provided."}
        
    try:
        # Adding header to prevent against bot detection
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(job_url, headers=headers, timeout=10)
        response.raise_for_status() # Throw an error if the page returns a 404 or 500
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strip unnecessary elements
        for element in soup(["script", "style", "nav", "footer", "header", "meta", "noscript"]):
            element.decompose()

        # Space separator ensures words don't get mashed together when HTML tags are removed
        raw_text = soup.get_text(separator=' ', strip=True)
        
        print(f"Successfully scraped: {raw_text}")
        
        # Update state
        return {"raw_job_posting": raw_text}
        
    except Exception as e:
        print(f"Scraper Agent Error: {e}")
        
        return {"raw_job_posting": f"Error scraping URL: {str(e)}"}
