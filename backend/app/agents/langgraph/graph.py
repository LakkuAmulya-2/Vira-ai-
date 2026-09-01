from langgraph.graph import END,StateGraph
from app.agents.contracts import AgentRequest,AgentResult,AgentName
from app.agents.orchestration.planner import AgentPlanner
from app.agents.orchestration.validator import confidence,validate_result
from app.agents.supervisor import SupervisorAgent
from app.agents.tools import AgentToolRegistry
from app.agents.langgraph.state import ViraAgentState
from app.agents.langgraph.checkpoint import get_checkpointer
class ViraLangGraph:
 def __init__(self):
  self.supervisor=SupervisorAgent();self.planner=AgentPlanner(self.supervisor);self.tools=AgentToolRegistry();g=StateGraph(ViraAgentState)
  for n,f in [("supervisor",self.supervise),("research_tools",self.research_tools),("specialist",self.specialist),("critic",self.critic),("human_review",self.human_review),("finalize",self.finalize)]:g.add_node(n,f)
  g.set_entry_point("supervisor");g.add_conditional_edges("supervisor",self.route_supervisor,{"research_tools":"research_tools","finalize":"finalize"});g.add_edge("research_tools","specialist");g.add_edge("specialist","critic");g.add_conditional_edges("critic",self.route_critic,{"research_tools":"research_tools","human_review":"human_review","finalize":"finalize"});g.add_edge("human_review","finalize");g.add_edge("finalize",END);self.graph=g.compile(checkpointer=get_checkpointer(),interrupt_before=["human_review"])
 def trace(self,s,e,extra=None):return [*s.get("trace",[]),{"event":e,**(extra or {})}]
 async def supervise(self,s):
  p=self.planner.create(AgentRequest(**s["request"]));tasks=[x.model_dump(mode="json") for x in p.tasks]
  return {"plan":p.model_dump(mode="json"),"tasks":tasks,"task_index":s.get("task_index",0),"results":s.get("results",[]),"evidence":s.get("evidence",[]),"trace":self.trace(s,"supervisor.planned",{"tasks":len(tasks)})}
 def route_supervisor(self,s):return "research_tools" if s.get("tasks") else "finalize"
 async def research_tools(self,s):
  i=s.get("task_index",0);tasks=s.get("tasks",[])
  if i>=len(tasks):return {}
  t=tasks[i];hits=[]
  for c in t.get("tool_calls",[]):hits.extend((await self.tools.execute(None,t["agent"],c["tool"],c.get("arguments",{}))).get("hits",[]))
  return {"evidence":[*s.get("evidence",[]),*hits],"trace":self.trace(s,"tools.completed",{"hits":len(hits)})}
 async def specialist(self,s):
  i=s.get("task_index",0);t=s["tasks"][i];r=await self.supervisor.run_agent(AgentName(t["agent"]),AgentRequest(**s["request"]));r.evidence=[x.get("citation",x) for x in s.get("evidence",[])];r=validate_result(r)
  return {"results":[*s.get("results",[]),r.model_dump(mode="json")],"task_index":i+1,"trace":self.trace(s,"specialist.completed",{"agent":t["agent"]})}
 async def critic(self,s):
  rows=[AgentResult(**x) for x in s.get("results",[])];review=bool(rows and rows[-1].requires_human_review)
  return {"requires_human_review":review,"trace":self.trace(s,"critic.reviewed",{"human_review":review})}
 def route_critic(self,s):
  if s.get("requires_human_review") and not s.get("human_approved",False):return "human_review"
  return "research_tools" if s.get("task_index",0)<len(s.get("tasks",[])) else "finalize"
 async def human_review(self,s):return {"trace":self.trace(s,"human_review.completed",{"approved":s.get("human_approved",False)})}
 async def finalize(self,s):
  rows=[AgentResult(**x) for x in s.get("results",[])];primary=AgentName(s["plan"]["primary_agent"]);final=next((x for x in reversed(rows) if x.agent==primary),rows[-1] if rows else AgentResult(agent=primary,answer="Unable to complete grounded execution.",requires_human_review=True))
  return {"final":{**final.model_dump(mode="json"),"confidence":confidence(rows)},"trace":self.trace(s,"finalized")}
