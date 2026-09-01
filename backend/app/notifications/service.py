from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import StudentAlert,NotificationPreference
from app.notifications.contracts import AlertCreate,NotificationPreferenceInput

async def emit(db:AsyncSession,student_id:str,payload:AlertCreate):
    row=await db.scalar(select(StudentAlert).where(StudentAlert.dedupe_key==payload.dedupe_key))
    if row:return row
    row=StudentAlert(student_id=student_id,**payload.model_dump());db.add(row);await db.commit();await db.refresh(row);return row
async def list_alerts(db:AsyncSession,student_id:str,limit:int=50):
    return (await db.scalars(select(StudentAlert).where(StudentAlert.student_id==student_id).order_by(StudentAlert.created_at.desc()).limit(limit))).all()
async def preferences(db:AsyncSession,student_id:str):
    row=await db.scalar(select(NotificationPreference).where(NotificationPreference.student_id==student_id))
    if not row:row=NotificationPreference(student_id=student_id);db.add(row);await db.commit();await db.refresh(row)
    return row
async def update_preferences(db:AsyncSession,student_id:str,payload:NotificationPreferenceInput):
    row=await preferences(db,student_id)
    for k,v in payload.model_dump().items():setattr(row,k,v)
    await db.commit();await db.refresh(row);return row
