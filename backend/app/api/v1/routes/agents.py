from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agents.contracts import AgentRequest
from app.agents.supervisor import SupervisorAgent
from app.core.security import CurrentUser, get_current_user

router = APIRouter()
supervisor = SupervisorAgent()


class AgentRunRequest(BaseModel):
    message: str
    conversation_id: str | None = None


@router.post("/run")
async def run_agents(
    payload: AgentRunRequest,
    user: CurrentUser = Depends(get_current_user),
):
    request = AgentRequest(
        message=payload.message,
        user_id=user.id,
        conversation_id=payload.conversation_id,
    )
    results = await supervisor.run(request)
    return {"results": [result.model_dump() for result in results]}
