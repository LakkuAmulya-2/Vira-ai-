import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.contracts import AgentRequest,AgentResult
from app.agents.orchestration.contracts import ExecutionStatus,OrchestrationResponse,TaskResult
from app.agents.orchestration.planner import AgentPlanner
from app.agents.orchestration.validator import confidence,validate_result
from app.agents.supervisor import SupervisorAgent
from app.agents.tools import AgentToolRegistry
from app.models.agent_execution import AgentExecution,AgentTaskExecution
from app.student_intelligence.personalization import build_personalization_context

class AgentOrchestrator:
    def __init__(self,supervisor:SupervisorAgent|None=None):
        self.supervisor=supervisor or SupervisorAgent();self.planner=AgentPlanner(self.supervisor);self.tools=AgentToolRegistry()
    async def execute(self,db:AsyncSession,request:AgentRequest)->OrchestrationResponse:
        personalization=await build_personalization_context(db,request.user_id)
        plan=self.planner.create(request)
        execution=AgentExecution(user_id=request.user_id,conversation_id=request.conversation_id,status="RUNNING",primary_agent=plan.primary_agent.value,plan={**plan.model_dump(mode="json"),"personalization_available":personalization["available"]})
        db.add(execution);await db.commit();await db.refresh(execution)
        outputs=[]
        for task in plan.tasks:
            started=time.perf_counter();row=AgentTaskExecution(execution_id=execution.id,task_id=task.task_id,agent=task.agent.value,status="RUNNING",input={"objective":task.objective,"message":request.message,"student_context":personalization if personalization["available"] else {}});db.add(row);await db.commit()
            try:
                evidence=[]
                for call in task.tool_calls:
                    arguments={**call.arguments}
                    if personalization["available"]:
                        arguments.setdefault("country_code",personalization["student"].get("country_code"))
                    payload=await self.tools.execute(db,task.agent.value,call.tool,arguments)
                    evidence.extend([hit["citation"] for hit in payload.get("hits",[])])
                result=await self.supervisor.run_agent(task.agent,request)
                result.evidence=evidence;result.actions=list(dict.fromkeys([*result.actions,*[call.tool for call in task.tool_calls],"apply_student_constraints" if personalization["available"] else ""]))
                result=validate_result(result);elapsed=int((time.perf_counter()-started)*1000)
                row.status="COMPLETED";row.output=result.model_dump(mode="json");row.latency_ms=elapsed;await db.commit()
                outputs.append(TaskResult(task_id=task.task_id,agent=task.agent,status=ExecutionStatus.COMPLETED,result=result,latency_ms=elapsed))
            except Exception as exc:
                elapsed=int((time.perf_counter()-started)*1000);row.status="FAILED";row.error=str(exc);row.latency_ms=elapsed;await db.commit()
                outputs.append(TaskResult(task_id=task.task_id,agent=task.agent,status=ExecutionStatus.FAILED,error=str(exc),latency_ms=elapsed))
        successful=[x.result for x in outputs if x.result]
        final=next((r for r in reversed(successful) if r.agent==plan.primary_agent),successful[-1] if successful else AgentResult(agent=plan.primary_agent,answer="Unable to complete grounded execution.",requires_human_review=True))
        execution.status="COMPLETED" if successful else "FAILED";execution.final_result={**final.model_dump(mode="json"),"personalization":personalization["available"]};await db.commit()
        return OrchestrationResponse(plan=plan,results=outputs,final=final,confidence=confidence(successful))
