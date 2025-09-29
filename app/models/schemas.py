from pydantic import BaseModel
from typing import Optional

class AgencyResponse(BaseModel):
    agency_name: str
    agency_slug: str
    regulation_size_mb: float
    last_updated: Optional[str] = None

class AnalysisResponse(BaseModel):
    agencies: list[AgencyResponse]
    total_agencies: int
    total_size_mb: float