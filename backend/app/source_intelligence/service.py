from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.source_intelligence.contracts import SourceProfileCreate
from app.source_intelligence.policies import normalize_country_code,validate_source_url
from app.models.source_intelligence import SourceProfile,SourceRun

async def create_profile(db:AsyncSession,payload:SourceProfileCreate)->SourceProfile:
    obj=SourceProfile(**{**payload.model_dump(exclude={"base_url","country_code"}),"base_url":str(payload.base_url).rstrip("/"),"country_code":normalize_country_code(payload.country_code)})
    db.add(obj);await db.commit();await db.refresh(obj);return obj

async def list_profiles(db:AsyncSession,region:str|None=None,country_code:str|None=None):
    stmt=select(SourceProfile)
    if region:stmt=stmt.where(SourceProfile.region==region)
    if country_code:stmt=stmt.where(SourceProfile.country_code==normalize_country_code(country_code))
    return (await db.scalars(stmt.order_by(SourceProfile.name))).all()

async def prepare_run(db:AsyncSession,profile_id:str,url:str,job_id:str)->SourceRun:
    profile=await db.get(SourceProfile,profile_id)
    if profile is None:raise ValueError("Unknown source profile")
    if not profile.enabled:raise ValueError("Source profile is disabled")
    validate_source_url(profile.base_url,profile.allowed_paths,url)
    run=SourceRun(source_profile_id=profile.id,job_id=job_id,url=url,status="QUEUED",adapter_key=profile.adapter_key)
    db.add(run);await db.commit();await db.refresh(run);return run
