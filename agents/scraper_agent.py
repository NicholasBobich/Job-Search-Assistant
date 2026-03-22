from core import JobSearchState
import requests
from bs4 import BeautifulSoup


def scraper_agent(state: JobSearchState):
    
    print("Scraper Agent: Scraping job URL job listing details...")

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
        raw_job_text = soup.get_text(separator=' ', strip=True)
        
        print(f"Successfully scraped job text: {raw_job_text}")

        raw_about_text = None
        about_url = state.get("about_us_url")
        
        if about_url:
            try:
                response = requests.get(about_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for element in soup(["script", "style", "nav", "footer", "header", "meta", "noscript"]):
                    element.decompose()
                
                raw_about_text = soup.get_text(separator=' ', strip=True)
                print(f"Successfully scraped About text: {raw_about_text}")
            
            except Exception as e:
                print(f"Scraper Agent Warning: Failed to scrape About page: {e}")
                raw_about_text = "Failed to retrieve About page."

        print("Scraper Agent: Scraped job details successfully!")

        return {
            "raw_job_posting": raw_job_text,
            "raw_about_us": raw_about_text
        }
        
    except Exception as e:
        print(f"Scraper Agent Error: {e}")
        
        return {"raw_job_posting": f"Error scraping URL: {str(e)}"}
