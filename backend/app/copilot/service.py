from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.contracts import AgentRequest
from app.agents.orchestration.service import AgentOrchestrator
from app.copilot.actions import propose_actions
from app.copilot.context import build_context
from app.copilot.contracts import CopilotRequest,CopilotResponse
from app.models.copilot import CopilotAction,CopilotConversation,CopilotMessage
from app.models.student import StudentProfile

orchestrator=AgentOrchestrator()

async def chat(db:AsyncSession,user_id:str,payload:CopilotRequest)->CopilotResponse:
    student=await db.scalar(select(StudentProfile).where(StudentProfile.user_id==user_id))
    if not student:raise ValueError("Student profile not found")
    context=await build_context(db,user_id)
    conversation=None
    if payload.conversation_id:conversation=await db.get(CopilotConversation,payload.conversation_id)
    if not conversation:
        conversation=CopilotConversation(student_id=student.id,context_snapshot=context);db.add(conversation);await db.flush()
    db.add(CopilotMessage(conversation_id=conversation.id,role="USER",content=payload.message))
    enriched=payload.message+"\n\nStudent context:\n"+str(context)
    result=await orchestrator.execute(db,AgentRequest(message=enriched,user_id=user_id,conversation_id=conversation.id))
    result_data=result.model_dump(mode="json")
    answer=str(result_data.get("answer") or result_data.get("final_answer") or result_data)
    db.add(CopilotMessage(conversation_id=conversation.id,role="ASSISTANT",content=answer,metadata_json={"agent_result":result_data}))
    actions=propose_actions(payload.message,context);rows=[]
    for action in actions:
        row=CopilotAction(student_id=student.id,conversation_id=conversation.id,**action);db.add(row);rows.append(row)
    await db.commit()
    return CopilotResponse(conversation_id=conversation.id,message=answer,agent_result=result_data,proposed_actions=[{"id":x.id,"action_type":x.action_type,"title":x.title,"requires_confirmation":x.requires_confirmation,"status":x.status} for x in rows])
