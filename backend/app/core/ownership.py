from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import StudentProfile
async def student_for_user(db:AsyncSession,user_id:str)->StudentProfile:
    row=await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id))
    if not row:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student profile not found")
    return row
async def require_application_owner(db:AsyncSession,user_id:str,application_id:str):
    from app.models.application import Application
    student=await student_for_user(db,user_id);row=await db.get(Application,application_id)
    if not row or row.student_id!=student.id:raise HTTPException(status_code=404,detail="Application not found")
    return row
