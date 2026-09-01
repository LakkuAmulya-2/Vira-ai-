import re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.education import Institution,Course,Scholarship,EntranceExam

def normalize_name(value:str)->str:
    return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",value).lower()).strip()

MODEL_MAP={"institution":Institution,"course":Course,"scholarship":Scholarship,"entrance_exam":EntranceExam}

async def resolve_entity(db:AsyncSession,entity_type:str,entity_key:str,country_code:str|None)->str|None:
    model=MODEL_MAP.get(entity_type)
    if model is None:return None
    target=normalize_name(entity_key)
    rows=(await db.scalars(select(model))).all()
    for row in rows:
        if normalize_name(row.canonical_name)==target and (not country_code or not hasattr(row,"country_code") or row.country_code==country_code):
            return row.id
    return None
