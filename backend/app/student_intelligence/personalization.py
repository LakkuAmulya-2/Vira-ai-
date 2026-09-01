from sqlalchemy.ext.asyncio import AsyncSession
from app.student_intelligence.persistence import load_student_context
from app.student_intelligence.scoring import constraint_summary

async def build_personalization_context(db:AsyncSession,user_id:str)->dict:
    context=await load_student_context(db,user_id)
    if not context:return {"available":False,"reason":"Student profile not found"}
    return {"available":True,"student":context,"constraints":constraint_summary(context),"retrieval_filters":{"country_code":context.get("country_code")}}
