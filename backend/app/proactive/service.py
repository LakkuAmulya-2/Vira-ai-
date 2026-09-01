from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.application import Application
from app.models.student import StudentProfile
from app.deadlines.contracts import DeadlineSignal
from app.deadlines.intelligence import assess
from app.notifications.contracts import AlertCreate
from app.notifications.service import emit

async def scan_student_deadlines(db:AsyncSession,user_id:str)->list[dict]:
    student=await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id))
    if not student:return []
    apps=(await db.scalars(select(Application).where(Application.student_id==student.id,Application.deadline.is_not(None)))).all()
    results=[]
    for app in apps:
        signal=DeadlineSignal(entity_type=app.entity_type,entity_key=app.entity_key,title=app.title,deadline=app.deadline)
        assessment=assess(signal)
        if assessment.days_remaining<0:continue
        if assessment.priority in {"CRITICAL","HIGH"}:
            alert=await emit(db,student.id,AlertCreate(alert_type="DEADLINE",entity_type=app.entity_type,entity_key=app.entity_key,priority=assessment.priority,title=f"{app.title}: deadline approaching",body=f"{assessment.days_remaining} days remaining. {assessment.action}.",dedupe_key=f"deadline:{app.id}:{app.deadline}:{assessment.priority}"))
            results.append({"alert_id":alert.id,**assessment.model_dump(mode="json")})
    return results
