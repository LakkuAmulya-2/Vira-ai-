from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import CareerGoal, StudentInterest, StudentProfile, StudentSkill
from app.schemas.student import StudentProfileUpsert


async def upsert_student_profile(
    db: AsyncSession, user_id: str, payload: StudentProfileUpsert
) -> StudentProfile:
    result = await db.execute(select(StudentProfile).where(StudentProfile.user_id == user_id))
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = StudentProfile(
            user_id=user_id,
            date_of_birth=payload.date_of_birth,
            gender=payload.gender,
            country_code=payload.country_code,
            state=payload.state,
            city=payload.city,
            education_stage=payload.education_stage,
            preferred_countries=payload.preferred_countries,
            preferred_languages=payload.preferred_languages,
            budget_currency=payload.budget_currency,
            annual_budget_minor=payload.annual_budget_minor,
        )
        db.add(profile)
        await db.flush()
    else:
        for key, value in payload.model_dump(exclude={"interests", "skills", "goals"}).items():
            setattr(profile, key, value)

        await db.execute(StudentInterest.__table__.delete().where(StudentInterest.student_id == profile.id))
        await db.execute(StudentSkill.__table__.delete().where(StudentSkill.student_id == profile.id))
        await db.execute(CareerGoal.__table__.delete().where(CareerGoal.student_id == profile.id))

    db.add_all([
        *(StudentInterest(student_id=profile.id, **item.model_dump()) for item in payload.interests),
        *(StudentSkill(student_id=profile.id, **item.model_dump()) for item in payload.skills),
        *(CareerGoal(student_id=profile.id, **item.model_dump()) for item in payload.goals),
    ])
    await db.commit()
    await db.refresh(profile)
    return profile
