from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.contracts import AgentRequest
from app.agents.langgraph.graph import ViraLangGraph
from app.agents.langgraph.events import stream_events
class LangGraphAgentRuntime:
 def __init__(self):self.workflow=ViraLangGraph()
 def config(self,thread_id:str):return {"configurable":{"thread_id":thread_id}}
 def initial(self,request:AgentRequest,human_approved:bool=False):
  return {"request":request.model_dump(mode="json"),"user_id":request.user_id,"conversation_id":request.conversation_id,"messages":[],"results":[],"evidence":[],"task_index":0,"human_approved":human_approved}
 async def execute(self,db:AsyncSession,request:AgentRequest,human_approved:bool=False,thread_id:str|None=None)->dict:
  tid=thread_id or request.conversation_id or f"agent:{request.user_id}"
  return await self.workflow.graph.ainvoke(self.initial(request,human_approved),config=self.config(tid))
 async def stream(self,db:AsyncSession,request:AgentRequest,thread_id:str|None=None)->AsyncIterator[dict]:
  tid=thread_id or request.conversation_id or f"agent:{request.user_id}"
  async for event in stream_events(self.workflow.graph,self.initial(request),self.config(tid)):yield event
 async def resume(self,thread_id:str,human_approved:bool)->dict:
  return await self.workflow.graph.aupdate_state(self.config(thread_id),{"human_approved":human_approved})
