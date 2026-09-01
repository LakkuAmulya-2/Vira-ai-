from sqlalchemy.ext.asyncio import AsyncSession
from app.retrieval.contracts import RetrievalRequest
from app.retrieval.service import hybrid_search
from app.tools.knowledge.contracts import KnowledgeEvidence,KnowledgeSearchRequest,KnowledgeSearchResponse

async def search_verified_knowledge(db:AsyncSession,request:KnowledgeSearchRequest)->KnowledgeSearchResponse:
    result=await hybrid_search(db,RetrievalRequest(query=request.query,entity_type=request.entity_type,country_code=request.country_code,jurisdiction=request.jurisdiction,limit=request.limit))
    evidence=[KnowledgeEvidence(claim_id=hit.citation.claim_id or "",entity_type=hit.citation.entity_type,entity_key=hit.citation.entity_key,field=hit.citation.field,value=hit.value,source_name=hit.citation.source_name,source_url=hit.citation.source_url,country_code=hit.citation.country_code,jurisdiction=hit.citation.jurisdiction) for hit in result.hits]
    return KnowledgeSearchResponse(query=request.query,evidence=evidence,total=len(evidence))
