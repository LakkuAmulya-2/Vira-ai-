from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.models.jobs import BackgroundJob

router=APIRouter()

@router.get("/{job_id}")
async def get_job(job_id:str, db:AsyncSession=Depends(get_db), _:CurrentUser=Depends(get_current_user)):
    job=await db.get(BackgroundJob,job_id)
    if not job: raise HTTPException(status_code=404,detail="Job not found")
    return {"job_id":job.id,"status":job.status,"attempts":job.attempts,"max_attempts":job.max_attempts,"result":job.result,"last_error":job.last_error,"available_at":job.available_at}
