from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from app.retrieval.contracts import RetrievalRequest
from app.retrieval.service import hybrid_search

@dataclass(frozen=True)
class ToolDefinition:
    name:str
    description:str
    allowed_agents:set[str]

class AgentToolRegistry:
    def __init__(self):
        self._tools={"knowledge.search":ToolDefinition("knowledge.search","Search verified education knowledge",{"career","admissions","scholarship","exam","research","recommendation"})}
    def list_for(self,agent:str)->list[ToolDefinition]:
        return [tool for tool in self._tools.values() if agent in tool.allowed_agents]
    async def execute(self,db:AsyncSession,agent:str,name:str,arguments:dict):
        tool=self._tools.get(name)
        if tool is None or agent not in tool.allowed_agents:raise PermissionError("Tool is not allowed for agent")
        if name=="knowledge.search":
            return (await hybrid_search(db,RetrievalRequest(query=arguments["query"],country_code=arguments.get("country_code"),limit=arguments.get("limit",8)))).model_dump()
        raise ValueError("Unknown tool")
