import asyncio,json,structlog
from app.core.config import settings
from app.connectors.contracts import ConnectorJobRequest,ConnectorType
from app.connectors.worker import fetch_content_with_metadata
from app.db.session import SessionLocal
from app.jobs.service import mark_completed,mark_failed,mark_running
log=structlog.get_logger()

async def run_worker()->None:
    if not settings.redis_url:raise RuntimeError("REDIS_URL is required for worker execution")
    import redis.asyncio as redis
    client=redis.from_url(settings.redis_url,decode_responses=True)
    try:
        while True:
            item=await client.brpop("vira:connector:jobs",timeout=5)
            if item is None:continue
            _,raw=item;payload=json.loads(raw)
            async with SessionLocal() as db:
                Job=__import__("app.models.jobs",fromlist=["BackgroundJob"]).BackgroundJob
                job=await db.get(Job,payload["job_id"])
                if not job:continue
                await mark_running(db,job)
                try:
                    content,_,content_type=await fetch_content_with_metadata(payload["source_url"])
                    if payload.get("source_profile_id") and payload.get("source_run_id"):
                        from app.source_intelligence.pipeline import process_regional_source
                        run=await process_regional_source(db,payload["source_profile_id"],payload["source_run_id"],content,content_type)
                        result={"source_run_id":run.id,"status":run.status,"result":run.result}
                    else:
                        from app.connectors.service import run_connector_job
                        result_obj=await run_connector_job(ConnectorJobRequest(source_url=payload["source_url"],connector_type=ConnectorType(payload["connector_type"]),country_code=payload.get("country_code"),jurisdiction=payload.get("jurisdiction"),entity_type=payload.get("entity_type","education_source"),dry_run=False))
                        result={"status":result_obj.status,"source_url":result_obj.source_url}
                    await mark_completed(db,job,result);log.info("connector_job_completed",job_id=job.id)
                except Exception as exc:
                    retry=await mark_failed(db,job,str(exc))
                    log.warning("connector_job_retry_scheduled" if retry else "connector_job_dead_letter",job_id=job.id,error=str(exc))
    finally:await client.aclose()
if __name__=="__main__":asyncio.run(run_worker())
