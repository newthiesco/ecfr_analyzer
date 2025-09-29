import asyncio
from os import name
from typing import List, Dict
from app.core.ecfr_client import ECFRClient
import logging

logger = logging.getLogger(name)

class RegulationAnalyzer:
    def init(self):
        self.ecfr_client = ECFRClient()
        self._cache = None
        self._cache_timestamp = None
    
    async def analyze_all_agencies(self) -> List[Dict]:
        """Analyze regulations for all agencies"""
        agencies = self.ecfr_client.get_agencies()
        results = []
        
        for agency in agencies:
            try:
                agency_name = agency.get('name', 'Unknown')
                agency_slug = agency.get('slug', '')
                
                logger.info(f"Analyzing regulations for {agency_name}")
                
                # Get regulation data
                regulation_data = self.ecfr_client.get_agency_regulations(agency_slug)
                
                # Calculate size
                size_mb = self.ecfr_client.calculate_regulation_size(regulation_data)
                
                results.append({
                    'agency_name': agency_name,
                    'agency_slug': agency_slug,
                    'regulation_size_mb': size_mb,
                    'last_updated': regulation_data.get('last_updated', '')
                })
                
                # Small delay to be respectful to the API
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error analyzing agency {agency.get('name', 'Unknown')}: {e}")
                continue
        
        # Sort by size descending
        results.sort(key=lambda x: x['regulation_size_mb'], reverse=True)
        return results
    
    def get_cached_analysis(self):
        """Get cached analysis results"""
        return self._cache
    
    def update_cache(self, data):
        """Update cache with new analysis"""
        self._cache = data
        self._cache_timestamp = asyncio.get_event_loop().time()