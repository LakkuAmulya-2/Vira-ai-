import json
from fastapi import APIRouter,Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.contracts import AgentName,AgentRequest
from app.agents.orchestration.service import AgentOrchestrator
from app.agents.langgraph.runtime import LangGraphAgentRuntime
from app.core.security import CurrentUser,get_current_user
from app.db.session import get_db
router=APIRouter();orchestrator=AgentOrchestrator();runtime=LangGraphAgentRuntime()
class AgentRunRequest(BaseModel):
 message:str=Field(min_length=1,max_length=12000);conversation_id:str|None=None;allowed_agents:list[AgentName]|None=None
@router.post("/run")
async def run_agents(payload:AgentRunRequest,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
 request=AgentRequest(message=payload.message,user_id=user.id,conversation_id=payload.conversation_id,allowed_agents=payload.allowed_agents);result=await orchestrator.execute(db,request);return result.model_dump(mode="json")
@router.post("/stream")
async def stream_agents(payload:AgentRunRequest,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
 request=AgentRequest(message=payload.message,user_id=user.id,conversation_id=payload.conversation_id,allowed_agents=payload.allowed_agents)
 async def events():
  async for event in runtime.stream(db,request):
   yield "data: "+json.dumps(event,default=str)+"\n\n"
 return StreamingResponse(events(),media_type="text/event-stream")
