from fastapi import APIRouter
from app.agents.scholarship.contracts import ScholarshipMatchRequest
from app.agents.scholarship.service import match_scholarships

router = APIRouter()

@router.post("/match")
async def match_scholarships_endpoint(payload: ScholarshipMatchRequest):
    return match_scholarships(payload)
