import json
from os import name
import time
from typing import List, Dict, Any
import logging

from fastapi import requests

logger = logging.getLogger(name)

class ECFRClient:
    def init(self, base_url: str = "https://www.ecfr.gov/api"):
        self.base_url = base_url.rstrip('/')
    
    def get_agencies(self) -> List[Dict[str, Any]]:
        """Get list of all agencies from eCFR API"""
        try:
            response = requests.get(f"{self.base_url}/admin/v1/agencies.json")
            response.raise_for_status()
            return response.json().get('agencies', [])
        except requests.RequestException as e:
            logger.error(f"Error fetching agencies: {e}")
            return []
    
    def get_agency_regulations(self, agency: str) -> Dict[str, Any]:
        """Get regulations for a specific agency"""
        try:
            # Using the titles endpoint to get regulation content
            response = requests.get(
                f"{self.base_url}/versioner/v1/titles.json",
                params={'agency': agency}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching regulations for {agency}: {e}")
            return {}
    
    def calculate_regulation_size(self, regulation_data: Dict[str, Any]) -> float:
        """Calculate the size of regulation data in MB"""
        if not regulation_data:
            return 0.0
        
        # Convert the entire regulation data to JSON string and calculate size
        json_string = json.dumps(regulation_data)
        size_bytes = len(json_string.encode('utf-8'))
        size_mb = size_bytes / (1024 * 1024)
        
        return round(size_mb, 2)