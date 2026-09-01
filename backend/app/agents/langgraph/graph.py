from langgraph.graph import END,StateGraph
from app.agents.contracts import AgentRequest,AgentResult,AgentName
from app.agents.orchestration.planner import AgentPlanner
from app.agents.orchestration.validator import confidence,validate_result
from app.agents.supervisor import SupervisorAgent
from app.agents.tools import AgentToolRegistry
from app.agents.langgraph.state import ViraAgentState

class ViraLangGraph:
    def __init__(self):
        self.supervisor=SupervisorAgent();self.planner=AgentPlanner(self.supervisor);self.tools=AgentToolRegistry()
        graph=StateGraph(ViraAgentState)
        graph.add_node("plan",self.plan)
        graph.add_node("execute",self.execute)
        graph.add_node("finalize",self.finalize)
        graph.set_entry_point("plan")
        graph.add_edge("plan","execute")
        graph.add_conditional_edges("execute",self.next_step,{"execute":"execute","finalize":"finalize"})
        graph.add_edge("finalize",END)
        self.graph=graph.compile()
    async def plan(self,state:ViraAgentState):
        request=AgentRequest(**state["request"]);plan=self.planner.create(request)
        return {"plan":plan.model_dump(mode="json"),"tasks":[x.model_dump(mode="json") for x in plan.tasks],"task_index":0,"results":[]}
    async def execute(self,state:ViraAgentState):
        index=state.get("task_index",0);tasks=state["tasks"]
        if index>=len(tasks):return {}
        task=tasks[index];request=AgentRequest(**state["request"]);evidence=[]
        for call in task.get("tool_calls",[]):
            payload=await self.tools.execute(None,task["agent"],call["tool"],call.get("arguments",{}))
            evidence.extend([x["citation"] for x in payload.get("hits",[])])
        result=await self.supervisor.run_agent(AgentName(task["agent"]),request)
        result.evidence=evidence
        result=validate_result(result)
        return {"results":[*state.get("results",[]),result.model_dump(mode="json")],"task_index":index+1}
    def next_step(self,state:ViraAgentState):
        return "execute" if state.get("task_index",0)<len(state.get("tasks",[])) else "finalize"
    async def finalize(self,state:ViraAgentState):
        results=[AgentResult(**x) for x in state.get("results",[])]
        primary=AgentName(state["plan"]["primary_agent"])
        final=next((x for x in reversed(results) if x.agent==primary),results[-1] if results else AgentResult(agent=primary,answer="Unable to complete execution.",requires_human_review=True))
        return {"final":{**final.model_dump(mode="json"),"confidence":confidence(results)}}
