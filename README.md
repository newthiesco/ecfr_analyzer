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
