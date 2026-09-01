import asyncio, json, structlog
from app.core.config import settings
from app.connectors.contracts import ConnectorJobRequest, ConnectorType
from app.connectors.service import run_connector_job
from app.db.session import SessionLocal
from app.jobs.service import mark_completed, mark_failed, mark_running

log=structlog.get_logger()

async def run_worker()->None:
    if not settings.redis_url: raise RuntimeError("REDIS_URL is required for worker execution")
    import redis.asyncio as redis
    client=redis.from_url(settings.redis_url,decode_responses=True)
    try:
        while True:
            item=await client.brpop("vira:connector:jobs",timeout=5)
            if item is None: continue
            _,raw=item; payload=json.loads(raw)
            async with SessionLocal() as db:
                job=await db.get(__import__("app.models.jobs",fromlist=["BackgroundJob"]).BackgroundJob,payload["job_id"])
                if not job: continue
                await mark_running(db,job)
                try:
                    result=await run_connector_job(ConnectorJobRequest(source_url=payload["source_url"],connector_type=ConnectorType(payload["connector_type"]),country_code=payload.get("country_code"),jurisdiction=payload.get("jurisdiction"),entity_type=payload.get("entity_type","education_source"),dry_run=False))
                    await mark_completed(db,job,{"status":result.status,"source_url":result.source_url})
                    log.info("connector_job_completed",job_id=job.id)
                except Exception as exc:
                    retry=await mark_failed(db,job,str(exc))
                    if retry:
                        log.warning("connector_job_retry_scheduled",job_id=job.id,attempt=job.attempts)
                    else:
                        log.exception("connector_job_dead_letter",job_id=job.id,error=str(exc))
    finally: await client.aclose()

if __name__=="__main__": asyncio.run(run_worker())
