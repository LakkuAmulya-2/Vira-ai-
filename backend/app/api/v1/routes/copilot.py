from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser,get_current_user
from app.db.session import get_db
from app.copilot.contracts import CopilotRequest,ActionDecision
from app.copilot.service import chat
from app.models.copilot import CopilotAction,CopilotConversation,CopilotMessage
router=APIRouter()
@router.post("/chat")
async def copilot_chat(payload:CopilotRequest,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    try:return (await chat(db,user.id,payload)).model_dump(mode="json")
    except ValueError as e:raise HTTPException(status_code=404,detail=str(e))
@router.get("/conversations/{conversation_id}/messages")
async def messages(conversation_id:str,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    rows=(await db.scalars(select(CopilotMessage).where(CopilotMessage.conversation_id==conversation_id).order_by(CopilotMessage.created_at))).all()
    return [{"id":x.id,"role":x.role,"content":x.content,"created_at":x.created_at} for x in rows]
@router.get("/actions")
async def actions(user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    rows=(await db.scalars(select(CopilotAction).order_by(CopilotAction.created_at.desc()).limit(100))).all()
    return [{"id":x.id,"title":x.title,"type":x.action_type,"status":x.status,"requires_confirmation":x.requires_confirmation} for x in rows]
@router.post("/actions/{action_id}/decision")
async def decide(action_id:str,payload:ActionDecision,user:CurrentUser=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    row=await db.get(CopilotAction,action_id)
    if not row:raise HTTPException(status_code=404,detail="Action not found")
    row.status="APPROVED" if payload.approved else "REJECTED";await db.commit()
    return {"id":row.id,"status":row.status}
