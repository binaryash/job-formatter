# Job Formatter

A Python automation tool that fetches job postings, extracts structured data using AI (Gemini), aggregates company reviews, and exports a comprehensive Excel report.

## Features

- **Smart Parsing**: Extracts job details (Role, Experience, Location) from raw HTML using Gemini.
- **Review Aggregation**: Fetches and scores company reviews from Glassdoor, AmbitionBox, etc.
- **Excel Export**: Generates a formatted Excel report with multiple sheets (Summary, Jobs, Reviews).
- **Configurable**: Customize search preferences (location, experience, etc.) easily.

## Prerequisites

- Python 3.8 or higher
- A Google Gemini API Key (Free tier available)
- `uv` (Recommended for fast package management)

## Installation

1.  **Install `uv`** (if not already installed):

    ```
    # On macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # On Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2.  **Clone the repository**:

    ```
    git clone https://github.com/yourusername/job-formatter.git
    cd job-formatter
    ```

3.  **Create a virtual environment and install dependencies**:

    ```
    # Create virtual env and sync dependencies
    uv venv
    uv pip install -r requirements.txt
    
    # Activate the environment
    # macOS/Linux:
    source .venv/bin/activate
    # Windows:
    .venv\Scripts\activate
    ```

## Configuration

1.  **Create a `.env` file** in the root directory:

    ```
    # .env file

    # Required: Your Gemini API Key
    GEMINI_API_KEY=your_actual_api_key_here

    # Optional: Model selection (default is gemini-2.0-flash)
    GEMINI_MODEL=gemini-2.0-flash

    # Optional: Input/Output settings
    INPUT_FILE=job_links.txt
    ```

2.  **Add Job Links**:
    - Create a file named `job_links.txt` in the root directory.
    - Paste one job URL per line.
    - *Alternatively, use `job_links.xlsx` with a column named "URL".*
    
    
    Job Links need to be in this format in `job_links.txt`. Each line corresponds to one job link.  
    
    ```
    https://www.linkedin.com/jobs/view/123456789/
    https://jobs.lever.co/company/example-role
    https://boards.greenhouse.io/company/jobs/9876543
    https://www.naukri.com/job-listings-example-12345
    ```

## Usage

Run the script:

```
uv run main.py
```

### Output

The script will generate an Excel file containing:
- **Summary**: Quick stats and top job matches.
- **Jobs Summary**: detailed breakdown of every job link.
- **Company Reviews**: Aggregated review scores and comments.

## Project Structure

```
job-formatter/
├── main.py    # Main script
├── .env                # API keys (do not commit!)
├── .gitignore          # Ignored files
├── job_links.txt       # Input URLs
├── requirements.txt    # Dependencies
└── README.md           # This file
```

## License

GNU GPL 3
