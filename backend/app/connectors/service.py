from app.connectors.contracts import ConnectorJobRequest, ConnectorJobResponse
from app.connectors.worker import create_job_id, fetch_content

async def run_connector_job(request: ConnectorJobRequest) -> ConnectorJobResponse:
    job_id = create_job_id()
    if request.dry_run:
        return ConnectorJobResponse(job_id=job_id, status="DRY_RUN", source_url=str(request.source_url), dry_run=True)

    try:
        _, content_hash = await fetch_content(str(request.source_url))
        return ConnectorJobResponse(
            job_id=job_id,
            status=f"FETCHED:{content_hash[:12]}",
            source_url=str(request.source_url),
            dry_run=False,
        )
    except Exception:
        return ConnectorJobResponse(job_id=job_id, status="FAILED", source_url=str(request.source_url), dry_run=False)
