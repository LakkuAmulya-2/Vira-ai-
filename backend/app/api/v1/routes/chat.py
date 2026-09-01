from fastapi import APIRouter
from app.agents.supervisor.contracts import SupervisorRequest
from app.agents.supervisor.service import route_request

router = APIRouter()

@router.post("/")
async def chat_with_vira(payload: SupervisorRequest):
    return route_request(payload)
