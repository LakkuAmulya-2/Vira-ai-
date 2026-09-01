from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.connectors.contracts import ConnectorJobRequest
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.jobs.queue import enqueue_connector_job
from app.jobs.service import create_job

router=APIRouter()

@router.post("/run", status_code=202)
async def run_connector(payload:ConnectorJobRequest, db:AsyncSession=Depends(get_db), _:CurrentUser=Depends(get_current_user)):
    message={"source_url":str(payload.source_url),"connector_type":payload.connector_type.value,"country_code":payload.country_code,"jurisdiction":payload.jurisdiction,"entity_type":payload.entity_type}
    job=await create_job(db,"CONNECTOR",message)
    await enqueue_connector_job({**message,"job_id":job.id})
    return {"job_id":job.id,"status":"QUEUED","source_url":message["source_url"],"dry_run":payload.dry_run}
