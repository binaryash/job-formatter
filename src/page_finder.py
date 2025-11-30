"""
Page Finder: Reads company list -> Gemini grounding search -> Career page URLs
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Import Genai class from main.py
sys.path.append(str(Path(__file__).parent.parent))
from main import Genai

load_dotenv()


class CareerPageFinder:
    """Find company career pages using Gemini grounding."""

    def __init__(self):
        self.genai_client = Genai()

    def find_career_page(self, company_name):
        """Find career page URL for a company using Gemini grounding."""
        system_prompt = """You are a career page URL finder. Your ONLY task is to find the official careers/jobs page URL for companies.

CRITICAL RULES:
- Return ONLY the direct career page URL (e.g., https://company.com/careers)
- Do NOT return the company homepage
- Do NOT return LinkedIn, Indeed, or job board URLs
- Do NOT return any explanation or additional text
- If no career page exists, return "NOT_FOUND"
- Return only ONE URL per company

Valid examples:
- https://google.com/careers
- https://stripe.com/jobs
- https://netflix.jobs

Invalid examples (DO NOT RETURN):
- https://company.com (homepage)
- https://linkedin.com/company/xyz
- https://indeed.com/company/xyz"""

        user_prompt = f"Find the official career page URL for: {company_name}"

        try:
            response = self.genai_client.send_request(
                system_prompt, user_prompt, use_search=True
            )
            return response.strip()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def process_company_list(self, input_file, output_file="career_pages.txt"):
        """Process list of companies and find their career pages."""
        print("=" * 60)
        print("CAREER PAGE FINDER")
        print("=" * 60)
        print(f"[+] Gemini Model: {self.genai_client.model}")
        print(f"[+] Using grounding search: Enabled")
        print()

        # Read company names
        if not os.path.exists(input_file):
            print(f"[!] Input file not found: {input_file}")
            return

        with open(input_file, "r", encoding="utf-8") as f:
            companies = [line.strip() for line in f if line.strip()]

        if not companies:
            print(f"[!] No companies found in {input_file}")
            return

        print(f"[+] Found {len(companies)} companies to process\n")

        # Process each company
        results = []
        for idx, company in enumerate(companies, 1):
            print(f"[{idx}/{len(companies)}] Searching: {company}")

            career_page = self.find_career_page(company)

            if career_page.startswith("ERROR"):
                print(f"  [!] {career_page}")
                results.append(f"{company} | ERROR")
            elif career_page == "NOT_FOUND":
                print(f"  [!] No career page found")
                results.append(f"{company} | NOT_FOUND")
            elif career_page.startswith("http"):
                print(f"  [+] Found: {career_page}")
                results.append(f"{company} | {career_page}")
            else:
                print(f"  [?] Unexpected response: {career_page[:100]}")
                results.append(f"{company} | {career_page}")

            print()

        # Write results
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Company | Career Page URL\n")
            f.write("=" * 60 + "\n")
            for result in results:
                f.write(result + "\n")

        print("=" * 60)
        print(f"[+] SUCCESS! Results saved to: {output_file}")
        print(f"[+] Total companies processed: {len(companies)}")
        print(
            f"[+] Found: {sum(1 for r in results if 'http' in r and 'ERROR' not in r)}"
        )
        print(f"[+] Not found: {sum(1 for r in results if 'NOT_FOUND' in r)}")
        print(f"[+] Errors: {sum(1 for r in results if 'ERROR' in r)}")
        print("=" * 60)


def main():
    """Main execution."""
    try:
        finder = CareerPageFinder()

        # Look for input file in parent directory (same location as main.py)
        input_file = os.getenv("COMPANY_LIST_FILE", "../job_name_list.txt")

        # Alternative file names to check
        possible_files = [
            input_file,
            "../company_list.txt",
            "../job_name_list.txt",
            "job_name_list.txt",
            "company_list.txt",
        ]

        selected_file = None
        for file_path in possible_files:
            if os.path.exists(file_path):
                selected_file = file_path
                break

        if not selected_file:
            print("[!] No input file found. Create one of these files:")
            print("  - job_name_list.txt")
            print("  - company_list.txt")
            print("\nFormat: One company name per line")
            return

        # Output to parent directory
        output_file = "../career_pages.txt"

        finder.process_company_list(selected_file, output_file)

    except Exception as e:
        print(f"[!] Fatal error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
