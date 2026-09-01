from uuid import uuid4
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser,get_current_user,require_admin
from app.db.session import get_db
from app.jobs.queue import enqueue_connector_job
from app.source_intelligence.contracts import SourceProfileCreate,SourceRunRequest,SourceRunResponse
from app.source_intelligence.service import create_profile,list_profiles,prepare_run

router=APIRouter()

@router.post("/profiles",status_code=201)
async def create_source_profile(payload:SourceProfileCreate,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)):
    return await create_profile(db,payload)

@router.get("/profiles")
async def get_source_profiles(region:str|None=None,country_code:str|None=None,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(get_current_user)):
    return await list_profiles(db,region,country_code)

@router.post("/runs",status_code=202,response_model=SourceRunResponse)
async def run_source(payload:SourceRunRequest,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)):
    job_id=str(uuid4())
    try:run=await prepare_run(db,payload.source_profile_id,str(payload.url),job_id)
    except ValueError as exc:raise HTTPException(status_code=422,detail=str(exc)) from exc
    await enqueue_connector_job({"job_id":job_id,"source_url":str(payload.url),"connector_type":"WEB","country_code":None,"jurisdiction":None,"entity_type":"education_source","source_profile_id":run.source_profile_id,"source_run_id":run.id})
    return SourceRunResponse(job_id=job_id,status=run.status,adapter_key=run.adapter_key)
