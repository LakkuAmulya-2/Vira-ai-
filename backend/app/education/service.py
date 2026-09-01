from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.education import Country, Institution, Course, Program, Scholarship, EntranceExam

async def create_entity(db:AsyncSession, model, payload:dict):
    obj=model(**payload); db.add(obj); await db.commit(); await db.refresh(obj); return obj

async def get_entity(db:AsyncSession, model, entity_id:str):
    return await db.get(model,entity_id)

async def search_entities(db:AsyncSession, model, query:str|None=None, country_code:str|None=None, limit:int=20):
    stmt=select(model)
    if query and hasattr(model,"canonical_name"): stmt=stmt.where(model.canonical_name.ilike(f"%{query}%"))
    if country_code and hasattr(model,"country_code"): stmt=stmt.where(model.country_code==country_code.upper())
    return (await db.scalars(stmt.limit(min(limit,100)))).all()
