from fastapi import APIRouter
from app.agents.college.contracts import CollegeMatchRequest
from app.agents.college.service import match_colleges

router = APIRouter()

@router.post("/match")
async def match_colleges_endpoint(payload: CollegeMatchRequest):
    return match_colleges(payload)
