from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agents.runtime import AgentRuntime
from app.agents.supervisor import SupervisorAgent
from app.core.security import CurrentUser, get_current_user
from app.workflows.student_journey.contracts import JourneyRequest
from app.workflows.student_journey.orchestrator import StudentJourneyWorkflow

router = APIRouter()
workflow = StudentJourneyWorkflow(AgentRuntime(SupervisorAgent()))


class StartJourneyRequest(BaseModel):
    conversation_id: str | None = None


@router.post("/start")
async def start_journey(
    payload: StartJourneyRequest,
    user: CurrentUser = Depends(get_current_user),
):
    return (
        await workflow.run(
            JourneyRequest(user_id=user.id, conversation_id=payload.conversation_id)
        )
    ).model_dump(mode="json")
