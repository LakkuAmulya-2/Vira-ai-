from sqlalchemy import select
from app.connectors.contracts import ConnectorJobRequest,ConnectorJobResponse
from app.connectors.worker import create_job_id,fetch_content_with_metadata
from app.db.session import SessionLocal
from app.ingestion.contracts import IngestionRequest
from app.ingestion.service import ingest_content
from app.models.knowledge import DataSource

async def run_connector_job(request:ConnectorJobRequest)->ConnectorJobResponse:
    job_id=create_job_id()
    if request.dry_run:return ConnectorJobResponse(job_id=job_id,status="DRY_RUN",source_url=str(request.source_url),dry_run=True)
    content,_,content_type=await fetch_content_with_metadata(str(request.source_url))
    async with SessionLocal() as db:
        source_url=str(request.source_url)
        source=await db.scalar(select(DataSource).where(DataSource.base_url==source_url.rstrip("/")))
        if source is None:
            source=DataSource(name=request.source_url.host,base_url=source_url.rstrip("/"),source_type=request.connector_type.value,country_code=request.country_code, jurisdiction=request.jurisdiction,verification_status="PENDING")
            db.add(source);await db.commit();await db.refresh(source)
        result=await ingest_content(db,IngestionRequest(source_id=source.id,url=request.source_url,country_code=request.country_code,entity_type=request.entity_type,force=False),content,content_type)
    return ConnectorJobResponse(job_id=job_id,status=f"{result.status}:{result.extracted_claims}",source_url=str(request.source_url),dry_run=False)
