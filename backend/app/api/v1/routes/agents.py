from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.agents.contracts import AgentRequest
from app.agents.runtime import AgentRuntime
from app.agents.supervisor import SupervisorAgent
from app.core.security import CurrentUser, get_current_user

router = APIRouter()
runtime = AgentRuntime(SupervisorAgent())


class AgentRunRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
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
    results = await runtime.execute(request)
    return {"results": [result.model_dump(mode="json") for result in results]}
