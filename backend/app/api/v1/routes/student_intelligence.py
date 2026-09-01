from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser,get_current_user
from app.db.session import get_db
from app.student_intelligence.contracts import StudentOnboardingInput
from app.student_intelligence.memory import upsert_memory
from app.student_intelligence.persistence import load_student_context,save_intelligence_profile
from app.student_intelligence.personalization import build_personalization_context
from app.student_intelligence.questions import next_questions
router=APIRouter()
@router.post("/profile")
async def build_student_intelligence_profile(payload:StudentOnboardingInput,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    try:profile=await save_intelligence_profile(db,user.id,payload)
    except ValueError as exc:raise HTTPException(status_code=409,detail=str(exc)) from exc
    return {"user_id":user.id,"profile":profile.model_dump(),"next_questions":next_questions(profile)}
@router.get("/context")
async def get_context(user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    return await build_personalization_context(db,user.id)
@router.get("/memory")
async def get_memory(user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    context=await load_student_context(db,user.id)
    if not context:raise HTTPException(status_code=404,detail="Student profile not found")
    return {"memory":context["memory"]}
@router.put("/memory/{namespace}/{memory_key}")
async def put_memory(namespace:str,memory_key:str,value:dict,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    context=await load_student_context(db,user.id)
    if not context:raise HTTPException(status_code=404,detail="Student profile not found")
    row=await upsert_memory(db,context["student_id"],namespace,memory_key,value)
    return {"id":row.id,"namespace":row.namespace,"memory_key":row.memory_key,"updated_at":row.updated_at.isoformat()}
