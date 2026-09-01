from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import audit
from app.core.ownership import require_application_owner
from app.core.security import CurrentUser,get_current_user
from app.db.session import get_db
from app.models.application import ApplicationDocument,ApplicationTask
from app.applications.contracts import ApplicationCreate,TaskCreate,DocumentCreate,ApplicationStatusUpdate
from app.applications import service
from app.applications.readiness import readiness
router=APIRouter()
@router.post("")
async def create(payload:ApplicationCreate,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    try:
        row=await service.create_application(db,user.id,payload);audit("application.created",user.id,"application",row.id);return row.__dict__
    except ValueError as e:raise HTTPException(status_code=409,detail=str(e))
@router.get("")
async def list_all(user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    return [{"id":x.id,"title":x.title,"status":x.status,"deadline":x.deadline,"entity_type":x.entity_type} for x in await service.list_applications(db,user.id)]
@router.post("/{application_id}/tasks")
async def create_task(application_id:str,payload:TaskCreate,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await require_application_owner(db,user.id,application_id);return (await service.add_task(db,application_id,payload)).__dict__
@router.post("/{application_id}/documents")
async def create_document(application_id:str,payload:DocumentCreate,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await require_application_owner(db,user.id,application_id);return (await service.add_document(db,application_id,payload)).__dict__
@router.patch("/{application_id}/status")
async def update_status(application_id:str,payload:ApplicationStatusUpdate,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    row=await require_application_owner(db,user.id,application_id);row.status=payload.status;await db.commit();audit("application.status_changed",user.id,"application",row.id,{"status":row.status});return {"id":row.id,"status":row.status}
@router.get("/{application_id}/readiness")
async def get_readiness(application_id:str,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await require_application_owner(db,user.id,application_id)
    tasks=(await db.scalars(select(ApplicationTask).where(ApplicationTask.application_id==application_id))).all();docs=(await db.scalars(select(ApplicationDocument).where(ApplicationDocument.application_id==application_id))).all();return readiness(tasks,docs)
@router.get("/{application_id}/timeline")
async def get_timeline(application_id:str,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await require_application_owner(db,user.id,application_id);return [{"event_type":x.event_type,"message":x.message,"created_at":x.created_at} for x in await service.timeline(db,application_id)]
