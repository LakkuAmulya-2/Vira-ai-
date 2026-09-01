from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.schemas.student import StudentProfileResponse, StudentProfileUpsert
from app.services.student_service import upsert_student_profile

router = APIRouter()


@router.put("/me/profile", response_model=StudentProfileResponse)
async def update_my_profile(
    payload: StudentProfileUpsert,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    profile = await upsert_student_profile(db, user.id, payload)
    return StudentProfileResponse(id=profile.id, updated_at=profile.updated_at.isoformat())
