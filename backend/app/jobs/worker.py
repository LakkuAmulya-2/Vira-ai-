import asyncio
import json
import structlog

from app.core.config import settings
from app.connectors.contracts import ConnectorJobRequest, ConnectorType
from app.connectors.service import run_connector_job

log = structlog.get_logger()

async def run_worker() -> None:
    if not settings.redis_url:
        raise RuntimeError("REDIS_URL is required for worker execution")
    import redis.asyncio as redis
    client = redis.from_url(settings.redis_url, decode_responses=True)
    try:
        while True:
            item = await client.brpop("vira:connector:jobs", timeout=5)
            if item is None:
                continue
            _, raw = item
            payload = json.loads(raw)
            try:
                await run_connector_job(ConnectorJobRequest(
                    source_url=payload["source_url"],
                    connector_type=ConnectorType(payload["connector_type"]),
                    country_code=payload.get("country_code"),
                    jurisdiction=payload.get("jurisdiction"),
                    entity_type=payload.get("entity_type", "education_source"),
                    dry_run=False,
                ))
                log.info("connector_job_completed", job_id=payload["job_id"])
            except Exception as exc:
                log.exception("connector_job_failed", job_id=payload["job_id"], error=str(exc))
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(run_worker())
