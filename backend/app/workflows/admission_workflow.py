from app.agents.contracts import AgentName, AgentRequest
from app.agents.runtime import AgentRuntime


class AdmissionWorkflow:
    def __init__(self, runtime: AgentRuntime) -> None:
        self.runtime = runtime

    async def run(self, request: AgentRequest):
        request.allowed_agents = [
            AgentName.CAREER,
            AgentName.ADMISSIONS,
            AgentName.SCHOLARSHIP,
            AgentName.EXAM,
            AgentName.RECOMMENDATION,
        ]
        return await self.runtime.execute(request)
