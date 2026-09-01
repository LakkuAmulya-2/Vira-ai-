import json
from fastapi import APIRouter,Depends,HTTPException
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
class ResumeRequest(BaseModel):
 thread_id:str=Field(min_length=1,max_length=200);approved:bool
@router.post("/run")
async def run_agents(payload:AgentRunRequest,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
 request=AgentRequest(message=payload.message,user_id=user.id,conversation_id=payload.conversation_id,allowed_agents=payload.allowed_agents);result=await orchestrator.execute(db,request);return result.model_dump(mode="json")
@router.post("/stream")
async def stream_agents(payload:AgentRunRequest,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
 request=AgentRequest(message=payload.message,user_id=user.id,conversation_id=payload.conversation_id,allowed_agents=payload.allowed_agents)
 async def events():
  try:
   async for event in runtime.stream(db,request):yield "data: "+json.dumps(event,default=str)+"\n\n"
  except Exception as exc:yield "event: error\ndata: "+json.dumps({"detail":"Agent stream failed","error":str(exc)})+"\n\n"
 return StreamingResponse(events(),media_type="text/event-stream",headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
@router.post("/resume")
async def resume_agents(payload:ResumeRequest,user:CurrentUser=Depends(get_current_user)):
 if not payload.thread_id.startswith((f"agent:{user.id}",user.id)):
  raise HTTPException(status_code=403,detail="Thread does not belong to current user")
 return await runtime.resume(payload.thread_id,payload.approved)
