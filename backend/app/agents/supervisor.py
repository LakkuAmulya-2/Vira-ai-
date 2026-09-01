from app.agents.contracts import AgentName, AgentPlan, AgentRequest, AgentResult
from app.agents.specialists import (
    AdmissionsAgent,
    CareerAgent,
    ExamAgent,
    RecommendationAgent,
    ResearchAgent,
    ScholarshipAgent,
)


class SupervisorAgent:
    def __init__(self) -> None:
        specialists = [
            CareerAgent(),
            AdmissionsAgent(),
            ScholarshipAgent(),
            ExamAgent(),
            ResearchAgent(),
            RecommendationAgent(),
        ]
        self._agents = {agent.name: agent for agent in specialists}

    def plan(self, request: AgentRequest) -> AgentPlan:
        text = request.message.lower()
        allowed = set(request.allowed_agents or list(self._agents))
        rules = [
            (("scholarship", "funding", "financial aid"), AgentName.SCHOLARSHIP),
            (("admission", "apply", "application"), AgentName.ADMISSIONS),
            (("exam", "entrance", "test preparation"), AgentName.EXAM),
            (("research", "find sources", "verify"), AgentName.RESEARCH),
            (("recommend", "best college", "best course"), AgentName.RECOMMENDATION),
        ]
        selected = AgentName.CAREER
        for keywords, agent in rules:
            if any(keyword in text for keyword in keywords):
                selected = agent
                break
        if selected not in allowed:
            raise PermissionError("Requested agent is not allowed for this execution")
        support = [AgentName.CAREER] if selected == AgentName.RECOMMENDATION else []
        return AgentPlan(primary_agent=selected, supporting_agents=support, reason="policy-based routing")

    async def run_agent(self, name: AgentName, request: AgentRequest) -> AgentResult:
        agent = self._agents.get(name)
        if agent is None:
            raise PermissionError(f"Unknown agent: {name}")
        return await agent.run(request.message, request.user_id)

    async def run(self, request: AgentRequest) -> list[AgentResult]:
        plan = self.plan(request)
        return [await self.run_agent(name, request) for name in [*plan.supporting_agents, plan.primary_agent]]
