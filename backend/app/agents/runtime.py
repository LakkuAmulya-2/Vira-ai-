import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from app.agents.contracts import AgentName, AgentRequest, AgentResult
from app.agents.supervisor import SupervisorAgent


@dataclass(frozen=True)
class RuntimePolicy:
    max_steps: int = 8
    timeout_seconds: float = 30.0
    max_parallel_agents: int = 3


class AgentRuntime:
    def __init__(self, supervisor: SupervisorAgent, policy: RuntimePolicy | None = None) -> None:
        self.supervisor = supervisor
        self.policy = policy or RuntimePolicy()

    async def execute(self, request: AgentRequest) -> tuple[AgentResult, ...]:
        plan = self.supervisor.plan(request)
        names = [*plan.supporting_agents, plan.primary_agent][: self.policy.max_parallel_agents]

        async def run_one(name: AgentName) -> AgentResult:
            return await self.supervisor.run_agent(name, request)

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*(run_one(name) for name in names)),
                timeout=self.policy.timeout_seconds,
            )
        except TimeoutError as exc:
            raise RuntimeError("Agent execution timed out") from exc

        return tuple(results)
