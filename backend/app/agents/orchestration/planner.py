from uuid import uuid4
from app.agents.contracts import AgentName,AgentRequest
from app.agents.orchestration.contracts import AgentTask,ExecutionPlan,ToolCall
from app.agents.supervisor import SupervisorAgent

class AgentPlanner:
    def __init__(self,supervisor:SupervisorAgent):self.supervisor=supervisor
    def create(self,request:AgentRequest)->ExecutionPlan:
        route=self.supervisor.plan(request)
        ordered=[*route.supporting_agents,route.primary_agent]
        tasks=[]
        for index,agent in enumerate(ordered):
            tasks.append(AgentTask(task_id=str(uuid4()),agent=agent,objective=f"Resolve {agent.value} aspects of the student request",tool_calls=[ToolCall(tool="knowledge.search",arguments={"query":request.message,"limit":8})],depends_on=[tasks[-1].task_id] if tasks else []))
        return ExecutionPlan(primary_agent=route.primary_agent,tasks=tasks,reason=route.reason,max_steps=max(1,len(tasks)))
