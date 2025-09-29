from os import name
from fastapi import FastAPI, BackgroundTasks
from app.api.endpoints import router as api_router
from app.services.analyzer import RegulationAnalyzer
import asyncio
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

analyzer = RegulationAnalyzer()

async def periodic_analysis():
    """Periodically update analysis data"""
    while True:
        try:
            logger.info("Performing periodic analysis update")
            results = await analyzer.analyze_all_agencies()
            analyzer.update_cache(results)
            logger.info("Periodic analysis completed")
        except Exception as e:
            logger.error(f"Error in periodic analysis: {e}")
        
        # Wait 24 hours before next update
        await asyncio.sleep(24 * 60 * 60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start background task
    task = asyncio.create_task(periodic_analysis())
    yield
    # Shutdown: Cancel background task
    task.cancel()

app = FastAPI(
    title="eCFR Regulation Analyzer API",
    description="API for analyzing Federal Regulations size across government agencies",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "eCFR Regulation Analyzer API",
        "endpoints": {
            "agency_sizes": "/api/v1/agencies/size",
            "health": "/api/v1/health"
        }
    }