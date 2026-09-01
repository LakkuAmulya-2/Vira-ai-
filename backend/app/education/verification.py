from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.education import EducationFact

async def verify_fact(db:AsyncSession,fact_id:str)->EducationFact|None:
    fact=await db.get(EducationFact,fact_id)
    if fact is None:return None
    fact.status="VERIFIED"
    fact.updated_at=datetime.now(timezone.utc)
    await db.commit(); await db.refresh(fact)
    return fact
