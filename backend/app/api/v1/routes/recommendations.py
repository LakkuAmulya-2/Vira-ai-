from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.models.student import StudentProfile
from app.recommendations.service import recommend

router = APIRouter()


@router.get("/me")
async def get_my_recommendations(
    entity_type: str = Query(pattern="^(career|course|college|scholarship)$"),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    result = await db.execute(select(StudentProfile).where(StudentProfile.user_id == user.id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")

    return (await recommend(db, student, entity_type=entity_type, limit=limit)).model_dump()
