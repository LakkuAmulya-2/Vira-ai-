from uuid import uuid4
from fastapi import APIRouter, Depends

from app.connectors.contracts import ConnectorJobRequest, ConnectorJobResponse
from app.core.security import CurrentUser, get_current_user
from app.jobs.queue import enqueue_connector_job

router = APIRouter()

@router.post("/run", status_code=202)
async def run_connector(
    payload: ConnectorJobRequest,
    _: CurrentUser = Depends(get_current_user),
):
    job_id = str(uuid4())
    await enqueue_connector_job({
        "job_id": job_id,
        "source_url": str(payload.source_url),
        "connector_type": payload.connector_type.value,
        "country_code": payload.country_code,
        "jurisdiction": payload.jurisdiction,
        "entity_type": payload.entity_type,
    })
    return ConnectorJobResponse(
        job_id=job_id,
        status="QUEUED",
        source_url=str(payload.source_url),
        dry_run=False,
    )
