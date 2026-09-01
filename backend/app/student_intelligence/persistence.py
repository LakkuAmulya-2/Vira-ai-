from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import StudentProfile
from app.models.student_intelligence import StudentAcademicRecord,StudentConstraint,StudentIntelligenceSnapshot,StudentMemory
from app.student_intelligence.contracts import StudentOnboardingInput,StudentIntelligenceProfile
from app.student_intelligence.profiler import build_profile

async def load_student_context(db:AsyncSession,user_id:str)->dict:
    student=await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id))
    if not student:return {}
    academics=(await db.scalars(select(StudentAcademicRecord).where(StudentAcademicRecord.student_id==student.id))).all()
    constraints=(await db.scalars(select(StudentConstraint).where(StudentConstraint.student_id==student.id))).all()
    memories=(await db.scalars(select(StudentMemory).where(StudentMemory.student_id==student.id))).all()
    return {"student_id":student.id,"country_code":student.country_code,"education_stage":student.education_stage,"preferred_countries":student.preferred_countries,"budget_currency":student.budget_currency,"annual_budget_minor":student.annual_budget_minor,"interests":[x.name for x in student.interests],"skills":[x.name for x in student.skills],"goals":[x.title for x in student.goals],"academic_records":[{"qualification":x.qualification,"board_or_system":x.board_or_system,"score":x.score,"score_scale":x.score_scale,"graduation_year":x.graduation_year} for x in academics],"constraints":[{"category":x.category,"value":x.value,"importance":x.importance} for x in constraints],"memory":{f"{x.namespace}.{x.memory_key}":x.value for x in memories}}

async def save_intelligence_profile(db:AsyncSession,user_id:str,payload:StudentOnboardingInput)->StudentIntelligenceProfile:
    student=await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id))
    if not student:raise ValueError("Student profile must be created before intelligence onboarding")
    profile=build_profile(payload)
    await db.execute(StudentAcademicRecord.__table__.delete().where(StudentAcademicRecord.student_id==student.id))
    await db.execute(StudentConstraint.__table__.delete().where(StudentConstraint.student_id==student.id))
    await db.execute(StudentIntelligenceSnapshot.__table__.update().where(StudentIntelligenceSnapshot.student_id==student.id).values(active=False))
    db.add_all([StudentAcademicRecord(student_id=student.id,**item.model_dump()) for item in payload.academic_records])
    db.add_all([StudentConstraint(student_id=student.id,**item.model_dump()) for item in payload.constraints])
    db.add(StudentIntelligenceSnapshot(student_id=student.id,profile_version=profile.profile_version,completeness_score=profile.completeness_score,profile=profile.model_dump(mode="json"),assumptions=profile.assumptions,active=True))
    await db.commit();return profile
