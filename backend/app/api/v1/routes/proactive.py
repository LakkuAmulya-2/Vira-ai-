from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser,get_current_user
from app.db.session import get_db
from app.proactive.service import scan_student_deadlines
router=APIRouter()
@router.post("/scan")
async def scan(user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    return {"alerts":await scan_student_deadlines(db,user.id)}
