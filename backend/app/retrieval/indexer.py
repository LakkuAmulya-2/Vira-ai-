from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge import KnowledgeClaim
from app.models.retrieval import KnowledgeEmbedding
from app.retrieval.embedding import build_claim_content,content_hash,deterministic_embedding

async def index_claim(db:AsyncSession,claim:KnowledgeClaim,model:str="local-deterministic-v1")->KnowledgeEmbedding:
    content=build_claim_content(claim.entity_type,claim.entity_key,claim.field,claim.value)
    digest=content_hash(content)
    row=await db.scalar(select(KnowledgeEmbedding).where(KnowledgeEmbedding.claim_id==claim.id))
    if row and row.content_hash==digest:return row
    vector=deterministic_embedding(content)
    if row is None:
        row=KnowledgeEmbedding(claim_id=claim.id,model=model,dimensions=len(vector),embedding=vector,content=content,content_hash=digest,status="READY");db.add(row)
    else:
        row.model=model;row.dimensions=len(vector);row.embedding=vector;row.content=content;row.content_hash=digest;row.status="READY"
    await db.flush();return row

async def index_verified_claims(db:AsyncSession,limit:int=1000)->int:
    rows=(await db.scalars(select(KnowledgeClaim).where(KnowledgeClaim.status=="VERIFIED").limit(limit))).all()
    for claim in rows:await index_claim(db,claim)
    await db.commit();return len(rows)
