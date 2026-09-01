from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser,get_current_user
from app.db.session import get_db
from app.models.student import StudentProfile
from app.notifications.contracts import NotificationPreferenceInput
from app.notifications.service import list_alerts,preferences,update_preferences
router=APIRouter()
async def student_id(db,user_id):
    s=await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id));return s.id if s else None
@router.get("/alerts")
async def alerts(user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    sid=await student_id(db,user.id);return [] if not sid else [{"id":x.id,"type":x.alert_type,"priority":x.priority,"status":x.status,"title":x.title,"body":x.body,"created_at":x.created_at} for x in await list_alerts(db,sid)]
@router.get("/preferences")
async def get_preferences(user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    sid=await student_id(db,user.id)
    return {} if not sid else (await preferences(db,sid)).__dict__
@router.put("/preferences")
async def put_preferences(payload:NotificationPreferenceInput,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    sid=await student_id(db,user.id)
    return {} if not sid else (await update_preferences(db,sid,payload)).__dict__
