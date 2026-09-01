from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import StudentProfile
from app.recommendations.service import recommend


async def recommend_verified_entities(
    db: AsyncSession,
    *,
    user_id: str,
    entity_type: str,
    limit: int = 20,
) -> dict:
    result = await db.execute(select(StudentProfile).where(StudentProfile.user_id == user_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise LookupError("Student profile not found")

    response = await recommend(db, student, entity_type=entity_type, limit=limit)
    return response.model_dump()
