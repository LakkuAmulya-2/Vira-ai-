from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.education import EducationFact

async def verified_facts(db:AsyncSession, entity_type:str, entity_id:str):
    stmt=select(EducationFact).where(EducationFact.entity_type==entity_type,EducationFact.entity_id==entity_id,EducationFact.status=="VERIFIED")
    return (await db.scalars(stmt)).all()
