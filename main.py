import os
from fastapi import FastAPI
import requests
import json
import asyncio
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="eCFR Analyzer API")

# In-memory cache
agency_cache = None

class ECFRClient:
    def __init__(self):
        self.base_url = "https://www.ecfr.gov/api"
    
    def get_agencies(self) -> List[Dict[str, Any]]:
        """Get list of agencies"""
        try:
            response = requests.get(f"{self.base_url}/admin/v1/agencies.json", timeout=30)
            response.raise_for_status()
            return response.json().get('agencies', [])
        except Exception as e:
            logger.error(f"Error fetching agencies: {e}")
            return []
    
    def calculate_size(self, data: Dict) -> float:
        """Calculate data size in MB"""
        if not data:
            return 0.0
        json_string = json.dumps(data)
        size_bytes = len(json_string.encode('utf-8'))
        return round(size_bytes / (1024 * 1024), 2)

async def analyze_regulations():
    """Analyze regulation sizes"""
    global agency_cache
    client = ECFRClient()
    agencies = client.get_agencies()
    results = []
    
    for agency in agencies[:10]:  # Limit to 10 agencies for demo
        try:
            name = agency.get('name', 'Unknown')
            slug = agency.get('slug', '')
            
            # Get regulation data
            response = requests.get(
                f"{client.base_url}/versioner/v1/titles.json",
                params={'agency': slug},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                size_mb = client.calculate_size(data)
                
                results.append({
                    'agency_name': name,
                    'agency_slug': slug,
                    'regulation_size_mb': size_mb,
                    'last_updated': data.get('last_updated', 'N/A')
                })
            
            await asyncio.sleep(0.1)  # Be nice to the API
            
        except Exception as e:
            logger.error(f"Error processing {agency.get('name', 'Unknown')}: {e}")
            continue
    
    agency_cache = sorted(results, key=lambda x: x['regulation_size_mb'], reverse=True)
    return agency_cache

@app.on_event("startup")
async def startup_event():
    """Run initial analysis on startup"""
    logger.info("Starting initial analysis...")
    await analyze_regulations()
    logger.info("Initial analysis completed")

@app.get("/")
async def root():
    return {
        "message": "eCFR Regulation Analyzer API",
        "status": "running",
        "endpoints": {
            "agency_sizes": "/api/v1/agencies/size",
            "health": "/api/v1/health",
            "update": "/api/v1/update"
        }
    }

@app.get("/api/v1/agencies/size")
async def get_agency_sizes():
    """Get regulation sizes for all agencies"""
    if agency_cache is None:
        await analyze_regulations()
    return agency_cache or []

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "service": "eCFR Analyzer"}

@app.get("/api/v1/update")
async def manual_update():
    """Trigger manual update"""
    results = await analyze_regulations()
    return {
        "message": "Data updated successfully",
        "agencies_analyzed": len(results)
    }

if __name__ == "main":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)