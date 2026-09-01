from fastapi import APIRouter,Depends
from pydantic import BaseModel,Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.contracts import AgentName,AgentRequest
from app.agents.orchestration.service import AgentOrchestrator
from app.core.security import CurrentUser,get_current_user
from app.db.session import get_db

router=APIRouter()
orchestrator=AgentOrchestrator()

class AgentRunRequest(BaseModel):
    message:str=Field(min_length=1,max_length=12000)
    conversation_id:str|None=None
    allowed_agents:list[AgentName]|None=None

@router.post("/run")
async def run_agents(payload:AgentRunRequest,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    request=AgentRequest(message=payload.message,user_id=user.id,conversation_id=payload.conversation_id,allowed_agents=payload.allowed_agents)
    result=await orchestrator.execute(db,request)
    return result.model_dump(mode="json")
