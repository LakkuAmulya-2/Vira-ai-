from fastapi import APIRouter, HTTPException
from app.agents.career.contracts import CareerDiscoveryRequest
from app.agents.career.service import discover_careers

router = APIRouter()

@router.post("/discover")
async def career_discovery(payload: CareerDiscoveryRequest):
    if not payload.profile:
        raise HTTPException(status_code=422, detail="A student intelligence profile is required.")
    return discover_careers(payload)
