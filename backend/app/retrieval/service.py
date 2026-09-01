from sqlalchemy import or_,select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge import DataSource,KnowledgeClaim,SourceDocument
from app.models.retrieval import KnowledgeEmbedding,RetrievalAudit
from app.retrieval.citations import citation_for
from app.retrieval.contracts import GroundedContextRequest,RetrievalHit,RetrievalRequest,RetrievalResponse
from app.retrieval.embedding import cosine_similarity,deterministic_embedding
from app.retrieval.indexer import index_claim

def lexical_score(query:str,claim:KnowledgeClaim)->float:
    terms=[x.lower() for x in query.split() if len(x)>1]
    hay=f"{claim.entity_type} {claim.entity_key} {claim.field} {claim.value}".lower()
    return sum(1 for term in terms if term in hay)/max(len(terms),1)

async def hybrid_search(db:AsyncSession,request:RetrievalRequest,user_id:str|None=None)->RetrievalResponse:
    stmt=(select(KnowledgeClaim,DataSource,SourceDocument,KnowledgeEmbedding)
      .join(DataSource,KnowledgeClaim.source_id==DataSource.id)
      .outerjoin(SourceDocument,KnowledgeClaim.document_id==SourceDocument.id)
      .outerjoin(KnowledgeEmbedding,KnowledgeEmbedding.claim_id==KnowledgeClaim.id)
      .where(KnowledgeClaim.status=="VERIFIED",DataSource.verification_status=="VERIFIED"))
    if request.entity_type:stmt=stmt.where(KnowledgeClaim.entity_type==request.entity_type)
    if request.country_code:stmt=stmt.where(KnowledgeClaim.country_code==request.country_code.upper())
    if request.jurisdiction:stmt=stmt.where(KnowledgeClaim.jurisdiction==request.jurisdiction)
    terms=[t for t in request.query.split() if len(t)>=2]
    if terms:
        predicates=[]
        for term in terms:
            pattern=f"%{term}%";predicates += [KnowledgeClaim.entity_key.ilike(pattern),KnowledgeClaim.field.ilike(pattern),KnowledgeClaim.entity_type.ilike(pattern)]
        stmt=stmt.where(or_(*predicates))
    rows=(await db.execute(stmt.limit(max(request.limit*8,100)))).all()
    qvec=deterministic_embedding(request.query);hits=[]
    for claim,source,document,embedding in rows:
        if embedding is None:embedding=await index_claim(db,claim)
        ls=lexical_score(request.query,claim);vs=max(0.0,cosine_similarity(qvec,embedding.embedding))
        score=request.lexical_weight*ls+request.vector_weight*vs
        citation=citation_for(claim,source,document)
        excerpt=f"{claim.entity_key} — {claim.field}: {claim.value}"
        hits.append(RetrievalHit(citation=citation,value=claim.value,score=score,lexical_score=ls,vector_score=vs,excerpt=excerpt))
    hits.sort(key=lambda x:x.score,reverse=True);hits=hits[:request.limit]
    context="\n".join(f"[{h.citation.citation_id}] {h.excerpt} | Source: {h.citation.source_name}" for h in hits)
    audit=RetrievalAudit(query_hash=__import__("hashlib").sha256(request.query.encode()).hexdigest(),user_id=user_id,filters={"entity_type":request.entity_type,"country_code":request.country_code,"jurisdiction":request.jurisdiction},result_count=len(hits))
    db.add(audit);await db.commit()
    return RetrievalResponse(query=request.query,hits=hits,context=context,total=len(hits))

async def grounded_context(db:AsyncSession,request:GroundedContextRequest,user_id:str|None=None)->RetrievalResponse:
    result=await hybrid_search(db,request,user_id)
    if len(result.context)>request.max_context_chars:result.context=result.context[:request.max_context_chars]
    return result
