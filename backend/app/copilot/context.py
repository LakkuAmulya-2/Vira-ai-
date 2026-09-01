from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.application import Application
from app.models.student import StudentProfile
from app.student_intelligence.persistence import load_student_context
async def build_context(db:AsyncSession,user_id:str)->dict:
    intelligence=await load_student_context(db,user_id)
    student=await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id))
    apps=[]
    if student:
        rows=(await db.scalars(select(Application).where(Application.student_id==student.id))).all()
        apps=[{"id":x.id,"title":x.title,"status":x.status,"deadline":x.deadline.isoformat() if x.deadline else None} for x in rows]
    return {"student":intelligence or {},"applications":apps}
