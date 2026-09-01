from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.source_intelligence import SourceProfile,SourceRun
from app.models.knowledge import DataSource,SourceDocument,KnowledgeClaim
from app.models.education import EducationFact
from app.source_intelligence.adapters import get_adapter
from app.source_intelligence.adapters.base import AdapterContext
from app.ingestion.canonicalizer import resolve_entity
from app.ingestion.contracts import IngestionRequest
from app.ingestion.service import ingest_content

async def process_regional_source(db:AsyncSession,profile_id:str,run_id:str,content:str,content_type:str|None):
    profile=await db.get(SourceProfile,profile_id)
    run=await db.get(SourceRun,run_id)
    if not profile or not run:raise ValueError("Source profile or run not found")
    run.status="PROCESSING";await db.commit()
    source=await db.scalar(select(DataSource).where(DataSource.base_url==profile.base_url))
    if source is None:
        source=DataSource(name=profile.name,base_url=profile.base_url,source_type=profile.category,country_code=profile.country_code,verification_status="PENDING")
        db.add(source);await db.commit();await db.refresh(source)
    result=await ingest_content(db,IngestionRequest(source_id=source.id,url=run.url,country_code=profile.country_code,entity_type=profile.entity_type,force=False),content,content_type)
    adapter=get_adapter(profile.adapter_key)
    title,claims=adapter.extract(content,content_type,AdapterContext(profile.region,profile.country_code,profile.category,profile.entity_type))
    added=0
    for item in claims:
        existing=await db.scalar(select(KnowledgeClaim).where(KnowledgeClaim.source_id==source.id,KnowledgeClaim.entity_type==item.entity_type,KnowledgeClaim.entity_key==item.entity_key,KnowledgeClaim.field==item.field))
        if existing is None:
            db.add(KnowledgeClaim(entity_type=item.entity_type,entity_key=item.entity_key,field=item.field,value=item.value,source_id=source.id,country_code=profile.country_code,status="PENDING"));added+=1
    run.status="COMPLETED";run.result={"document_id":result.document_id,"changed":result.changed,"claims":added,"adapter":profile.adapter_key}
    await db.commit();return run
