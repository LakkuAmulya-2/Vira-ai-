from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.jobs import BackgroundJob

async def create_job(db: AsyncSession, job_type: str, payload: dict, max_attempts: int = 5) -> BackgroundJob:
    job = BackgroundJob(job_type=job_type, payload=payload, max_attempts=max_attempts)
    db.add(job); await db.commit(); await db.refresh(job); return job

async def mark_running(db: AsyncSession, job: BackgroundJob) -> None:
    job.status="RUNNING"; job.attempts += 1; job.started_at=datetime.now(timezone.utc); await db.commit()

async def mark_completed(db: AsyncSession, job: BackgroundJob, result: dict) -> None:
    job.status="COMPLETED"; job.result=result; job.completed_at=datetime.now(timezone.utc); job.last_error=None; await db.commit()

async def mark_failed(db: AsyncSession, job: BackgroundJob, error: str) -> bool:
    job.last_error=error
    if job.attempts >= job.max_attempts:
        job.status="DEAD_LETTER"; await db.commit(); return False
    delay=min(300, 2 ** job.attempts)
    job.status="RETRY_SCHEDULED"; job.available_at=datetime.now(timezone.utc)+timedelta(seconds=delay)
    await db.commit(); return True
