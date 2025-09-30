# ecfr-analyzer

Small web API to analyze the eCFR and estimate the size (in MB) of regulations per agency/title.

## What this project does
- Exposes `/api/agency-sizes` returning a JSON payload with agency names and estimated regulation sizes (MB).
- Caches results to disk and refreshes every 24 hours so the API reflects changes to the eCFR within 24 hours without changing source code.

## How it works (brief)
- The app scrapes the eCFR title/index page, follows candidate links for each title/agency, downloads a bounded number of pages per agency, and sums the bytes of responses to estimate size. This is a best-effort approach; if a bulk API is available you may substitute that code path for more exact results.
- Results are cached at `/tmp/ecfr_agency_size_cache.json` and rebuilt when older than 24 hours.

## Running locally
```bash
Make sure you’re in the project directory

cd ecfr-analyzer

Create & activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate     # on macOS/Linux
# or
.venv\Scripts\activate        # on Windows PowerShell

Install dependencies
pip install -r requirements.txt
This will install:

fastapi==0.104.1
uvicorn[standard]==0.24.0
requests==2.31.0

Run the app
python -m uvicorn app.main:app --reload

Quick sanity check
Run:
python -c "import requests; print('✅ requests installed')"


You can hit the endpoints from test.py 
```python test.py


Root:
👉 http://127.0.0.1:8000/

Agency sizes:
👉 http://127.0.0.1:8000/api/v1/agencies/size

Health check:
👉 http://127.0.0.1:8000/api/v1/health

Manual refresh:
👉 http://127.0.0.1:8000/api/v1/update


## Remote deployment
You can deploy this app to any server that supports Python and has internet access. Here are general steps:
1. Choose a hosting provider (e.g., Render).
2. Set up a new web service with Python environment.
3. Clone this repository to the server.
4. Install dependencies using `pip install -r requirements.txt`.
5. Configure the service to run `uvicorn app.main:app --host 0.
0.0.0 --port $PORT` (adjust host/port as needed).
6. Start the service and verify it’s running by accessing the endpoints.
7. Monitor logs for any issues and ensure the cache refreshes as expected.
8. Test the API endpoints to ensure they return the expected data.
9. Regularly update dependencies and the codebase as needed.


==============================================================================

🚀 Deploying to Render (FastAPI + Uvicorn)

Render makes it easy to host FastAPI apps.
1. Push Your Code to GitHub

Ensure the project (ecfr-analyzer/) is in a GitHub repo.

Commit and push all changes, including requirements.txt and build.sh.

2. Create a New Web Service on Render

Log in to Render
Go to the Render dashboard and click "New" > "Web Service".
Connect your GitHub repo and select the repository containing your FastAPI app.
Select your repo (ecfr-analyzer) and branch (e.g., main).

3. Configure the Service
Environment: Python 3

Build Command:
chmod +x build.sh && ./build.sh
Configure the service to run:
uvicorn app.main:app --host 0.0.0.0 --port 8000

Test API endpoints (/, /api/v1/agencies/size, /api/v1/health, /api/v1/update) to confirm correct responses.

Maintain the app by updating dependencies and code as needed.


