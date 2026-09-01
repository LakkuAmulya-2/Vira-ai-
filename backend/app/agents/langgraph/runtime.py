from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.contracts import AgentRequest
from app.agents.langgraph.graph import ViraLangGraph
class LangGraphAgentRuntime:
    def __init__(self):self.workflow=ViraLangGraph()
    async def execute(self,db:AsyncSession,request:AgentRequest)->dict:
        initial={"request":request.model_dump(mode="json"),"user_id":request.user_id,"conversation_id":request.conversation_id,"messages":[]}
        return await self.workflow.graph.ainvoke(initial)
