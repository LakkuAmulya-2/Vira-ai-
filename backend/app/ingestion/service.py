import hashlib
from datetime import datetime,timezone
from urllib.parse import urlparse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ingestion.contracts import IngestionRequest,IngestionResult
from app.ingestion.parser import parse_document
from app.ingestion.extractor import extract_claims
from app.ingestion.canonicalizer import resolve_entity
from app.models.knowledge import DataSource,SourceDocument,KnowledgeClaim
from app.models.education import EducationFact

async def ingest_content(db:AsyncSession,request:IngestionRequest,content:str,content_type:str|None=None)->IngestionResult:
    source=await db.get(DataSource,request.source_id)
    if source is None: raise ValueError("Unknown source_id")
    url=str(request.url)
    digest=hashlib.sha256(content.encode("utf-8")).hexdigest()
    document=await db.scalar(select(SourceDocument).where(SourceDocument.url==url))
    if document and document.content_hash==digest and not request.force:
        return IngestionResult(document_id=document.id,changed=False,status="UNCHANGED",extracted_claims=0)
    if document is None:
        document=SourceDocument(source_id=source.id,url=url,status="PROCESSING")
        db.add(document); await db.flush()
    document.content_hash=digest; document.fetched_at=datetime.now(timezone.utc); document.status="PARSED"
    title,text,structured=parse_document(content,content_type)
    document.title=title
    claims=extract_claims(title,text,structured,request.entity_type)
    count=0
    for item in claims:
        existing=await db.scalar(select(KnowledgeClaim).where(KnowledgeClaim.entity_type==item.entity_type,KnowledgeClaim.entity_key==item.entity_key,KnowledgeClaim.field==item.field,KnowledgeClaim.source_id==source.id,KnowledgeClaim.document_id==document.id))
        if existing is None:
            existing=KnowledgeClaim(entity_type=item.entity_type,entity_key=item.entity_key,field=item.field,value=item.value,source_id=source.id,document_id=document.id,country_code=request.country_code,status="PENDING")
            db.add(existing); await db.flush(); count+=1
        entity_id=await resolve_entity(db,item.entity_type,item.entity_key,request.country_code)
        if entity_id:
            fact=await db.scalar(select(EducationFact).where(EducationFact.entity_type==item.entity_type,EducationFact.entity_id==entity_id,EducationFact.field==item.field,EducationFact.source_id==source.id))
            if fact is None:
                db.add(EducationFact(entity_type=item.entity_type,entity_id=entity_id,field=item.field,value=item.value,source_id=source.id,document_id=document.id,confidence=item.confidence,status="PENDING"))
    document.status="READY"
    await db.commit(); await db.refresh(document)
    return IngestionResult(document_id=document.id,changed=True,status="READY",extracted_claims=count)
