from sqlalchemy.ext.asyncio import AsyncSession
from app.retrieval.contracts import GroundedContextRequest
from app.retrieval.service import grounded_context

async def build_agent_context(db:AsyncSession,message:str,user_id:str|None=None,country_code:str|None=None)->dict:
    result=await grounded_context(db,GroundedContextRequest(query=message,country_code=country_code,limit=10,max_context_chars=8000),user_id)
    return {"context":result.context,"citations":[hit.citation.model_dump() for hit in result.hits]}
