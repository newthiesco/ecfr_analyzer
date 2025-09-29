from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.analyzer import RegulationAnalyzer
from app.models.schemas import AgencyResponse, AnalysisResponse
import logging
from typing import List

router = APIRouter()
analyzer = RegulationAnalyzer()

@router.get("/agencies/size", response_model=List[AgencyResponse])
async def get_agency_regulation_sizes():
    """Get regulation sizes for all agencies"""
    try:
        # Try to use cached data first
        cached_data = analyzer.get_cached_analysis()
        if cached_data:
            return cached_data
        
        # If no cache, perform analysis
        results = await analyzer.analyze_all_agencies()
        analyzer.update_cache(results)
        return results
        
    except Exception as e:
        logging.error(f"Error in get_agency_regulation_sizes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "eCFR Analyzer API"}