import pytest

from app.agents.contracts import AgentName, AgentRequest
from app.agents.supervisor import SupervisorAgent


@pytest.mark.asyncio
async def test_supervisor_routes_scholarship_request():
    supervisor = SupervisorAgent()
    request = AgentRequest(message="Find scholarships for engineering", user_id="user-1")
    plan = supervisor.plan(request)
    assert plan.primary_agent == AgentName.SCHOLARSHIP
