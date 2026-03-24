from dotenv import load_dotenv
load_dotenv()
import argparse
import sys
import os
from pypdf import PdfReader
from graph import workflow_app


def read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        print(f"Error: Could not find file at '{file_path}'")
        sys.exit(1)
        
    _, file_extension = os.path.splitext(file_path)
    
    try:
        if file_extension.lower() == '.pdf':
            print("Detected PDF resume. Reading file...")
            reader = PdfReader(file_path)
            extracted_text = ""
            for page in reader.pages:
                # Add a newline after each page to keep formatting cleaner
                extracted_text += page.extract_text() + "\n" 
            return extracted_text
        
        elif file_extension.lower() in ['.txt', '.md']:
            print("Detected Text/Markdown resume. Reading file...")
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        # Catch unsupported formats like .docx
        else:
            print(f"Error: Unsupported file type '{file_extension}'. Please use .txt, .md, or .pdf.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Job Search Assistant")
    parser.add_argument("--job", required=True, help="URL of the job posting")
    parser.add_argument("--resume", required=True, help="Path to your resume")
    parser.add_argument("--about", required=False, help="Optional: URL to the company's 'About Us' page")
    
    args = parser.parse_args()
    
    print("\nStarting the Job Search Assistant...")
    user_resume_text = read_file(args.resume)
    
    initial_state = {
        "job_url": args.job,
        "about_us_url": args.about,
        "user_resume": user_resume_text,
    }
    
    try:
        final_state = workflow_app.invoke(initial_state)
    except Exception as e:
        print(f"\nError occurred during execution: {e}")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(f"Match Score: {final_state.get('match_score')}/100")
    
    missing_keywords = final_state.get("missing_keywords", [])
    if missing_keywords:
        print(f"\nMissing Keywords: {', '.join(missing_keywords)}")
    else:
        print("\nNo critical keywords missing!")
        
    print("\n" + "="*50)
    print("SUGGESTED RESUME TWEAKS")
    print("="*50)
    for tweak in final_state.get("resume_tweaks", []):
        print(f"- {tweak}")
        
    print("\n" + "="*50)
    print("DRAFTED COVER LETTER")
    print("="*50)
    print(final_state.get("drafted_cover_letter"))
    
    # Optional: Save to file
    output_filename = "tweaks_and_cover_letter.txt"
    with open(output_filename, "w", encoding='utf-8') as f:
        f.write(f"# Cover Letter\n\n{final_state.get('drafted_cover_letter')}\n\n")
        f.write("# Resume Tweaks\n\n")
        for tweak in final_state.get("resume_tweaks", []):
            f.write(f"- {tweak}\n")
            
    print(f"\nSaved output to {output_filename}")

if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable is missing.")
        print("Please run: export GOOGLE_API_KEY='your_key' before executing.")
        sys.exit(1)
        
    main()
