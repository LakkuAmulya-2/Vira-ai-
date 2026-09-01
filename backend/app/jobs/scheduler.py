import asyncio, json
from datetime import datetime, timezone
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.jobs import BackgroundJob

async def dispatch_due_jobs() -> int:
    from app.jobs.queue import enqueue_connector_job
    async with SessionLocal() as db:
        jobs=(await db.scalars(select(BackgroundJob).where(BackgroundJob.status=="RETRY_SCHEDULED", BackgroundJob.available_at<=datetime.now(timezone.utc)))).all()
        for job in jobs:
            job.status="QUEUED"
            await enqueue_connector_job({**job.payload,"job_id":job.id})
        await db.commit()
        return len(jobs)

async def run_scheduler() -> None:
    while True:
        await dispatch_due_jobs()
        await asyncio.sleep(15)

if __name__=="__main__":
    asyncio.run(run_scheduler())
