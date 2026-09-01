from fastapi import APIRouter
from app.agents.admissions.contracts import AdmissionsPlanRequest
from app.agents.admissions.service import build_admissions_plan

router = APIRouter()

@router.post("/plan")
async def create_admissions_plan(payload: AdmissionsPlanRequest):
    return build_admissions_plan(payload)
