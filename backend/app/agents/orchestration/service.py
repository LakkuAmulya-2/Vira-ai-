import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.contracts import AgentRequest,AgentResult,AgentName
from app.agents.orchestration.contracts import ExecutionStatus,OrchestrationResponse,TaskResult
from app.agents.orchestration.planner import AgentPlanner
from app.agents.orchestration.validator import confidence
from app.agents.supervisor import SupervisorAgent
from app.agents.langgraph.runtime import LangGraphAgentRuntime
from app.models.agent_execution import AgentExecution,AgentTaskExecution
from app.student_intelligence.personalization import build_personalization_context

class AgentOrchestrator:
 def __init__(self,supervisor:SupervisorAgent|None=None):
  self.supervisor=supervisor or SupervisorAgent();self.planner=AgentPlanner(self.supervisor);self.runtime=LangGraphAgentRuntime()
 async def execute(self,db:AsyncSession,request:AgentRequest)->OrchestrationResponse:
  personalization=await build_personalization_context(db,request.user_id);plan=self.planner.create(request)
  execution=AgentExecution(user_id=request.user_id,conversation_id=request.conversation_id,status="RUNNING",primary_agent=plan.primary_agent.value,plan={**plan.model_dump(mode="json"),"runtime":"langgraph","personalization_available":personalization["available"]})
  db.add(execution);await db.commit();await db.refresh(execution);started=time.perf_counter()
  try:
   state=await self.runtime.execute(db,request)
   results=[AgentResult(**x) for x in state.get("results",[])]
   outputs=[]
   for i,result in enumerate(results):
    row=AgentTaskExecution(execution_id=execution.id,task_id=plan.tasks[i].task_id if i<len(plan.tasks) else str(i),agent=result.agent.value,status="COMPLETED",input={"message":request.message},output=result.model_dump(mode="json"))
    db.add(row);outputs.append(TaskResult(task_id=row.task_id,agent=result.agent,status=ExecutionStatus.COMPLETED,result=result,latency_ms=None))
   final=AgentResult(**state["final"])
   execution.status="COMPLETED";execution.final_result={**state["final"],"trace":state.get("trace",[]),"latency_ms":int((time.perf_counter()-started)*1000)}
   await db.commit()
   return OrchestrationResponse(plan=plan,results=outputs,final=final,confidence=state["final"].get("confidence",confidence(results)))
  except Exception as exc:
   execution.status="FAILED";execution.final_result={"error":str(exc)};await db.commit();raise
