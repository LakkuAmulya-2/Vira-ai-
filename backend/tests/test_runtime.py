import pytest

from app.agents.contracts import AgentRequest
from app.agents.runtime import AgentRuntime
from app.agents.supervisor import SupervisorAgent


@pytest.mark.asyncio
async def test_runtime_returns_specialist_result():
    runtime = AgentRuntime(SupervisorAgent())
    results = await runtime.execute(AgentRequest(message="Best course for my interests", user_id="u1"))
    assert len(results) >= 1
