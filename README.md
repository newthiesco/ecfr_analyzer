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
6. Ensure the server has write permissions to `/tmp` or adjust the cache path in `
app/main.py`.
7. Start the service and verify it’s running by accessing the endpoints.
8. Monitor logs for any issues and ensure the cache refreshes as expected.
9. Optionally set up a domain and SSL for secure access.
10. Test the API endpoints to ensure they return the expected data.
11. Set up monitoring and alerts for uptime and performance.
12. Regularly update dependencies and the codebase as needed.
13. Consider setting up automated tests and CI/CD for smoother deployments.
14. Document the deployment process for future reference.
15. Ensure compliance with any hosting provider policies regarding web scraping.
16. Backup the cache file periodically if necessary.
## Notes
- This is a basic implementation and may need adjustments based on specific requirements or changes in the eCFR website structure.
- Always check the eCFR website’s terms of service regarding web scraping.
- Consider adding error handling and logging for production use.
- You may want to implement rate limiting or delays between requests to avoid overloading the eCFR servers.
- For large-scale or frequent data retrieval, consider reaching out to the eCFR administrators for
access to bulk data or APIs.

