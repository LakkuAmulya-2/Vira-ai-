from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.application import Application,ApplicationTask,ApplicationDocument,ApplicationEvent
from app.models.student import StudentProfile
from app.applications.contracts import ApplicationCreate,TaskCreate,DocumentCreate

async def student(db,user_id):
    return await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id))
async def create_application(db,user_id,payload:ApplicationCreate):
    s=await student(db,user_id)
    if not s:raise ValueError("Student profile not found")
    row=Application(student_id=s.id,**payload.model_dump());db.add(row);await db.flush()
    db.add(ApplicationEvent(application_id=row.id,event_type="CREATED",message="Application journey created"))
    await db.commit();await db.refresh(row);return row
async def list_applications(db,user_id):
    s=await student(db,user_id)
    if not s:return []
    return (await db.scalars(select(Application).where(Application.student_id==s.id).order_by(Application.deadline))).all()
async def add_task(db,application_id,payload:TaskCreate):
    row=ApplicationTask(application_id=application_id,**payload.model_dump());db.add(row);await db.commit();await db.refresh(row);return row
async def add_document(db,application_id,payload:DocumentCreate):
    row=ApplicationDocument(application_id=application_id,document_type=payload.document_type,storage_key=payload.storage_key,status="READY" if payload.storage_key else "MISSING");db.add(row);await db.commit();await db.refresh(row);return row
async def timeline(db,application_id):
    return (await db.scalars(select(ApplicationEvent).where(ApplicationEvent.application_id==application_id).order_by(ApplicationEvent.created_at))).all()
