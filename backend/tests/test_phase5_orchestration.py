import pytest
from app.agents.contracts import AgentName,AgentRequest,AgentResult
from app.agents.orchestration.planner import AgentPlanner
from app.agents.orchestration.validator import confidence,validate_result
from app.agents.supervisor import SupervisorAgent
def test_planner_routes_scholarship():
    plan=AgentPlanner(SupervisorAgent()).create(AgentRequest(message="Find scholarship funding",user_id="u1"))
    assert plan.primary_agent==AgentName.SCHOLARSHIP
    assert plan.tasks[0].tool_calls[0].tool=="knowledge.search"
def test_confidence_penalizes_review():
    result=AgentResult(agent=AgentName.ADMISSIONS,answer="x",requires_human_review=True)
    assert confidence([result])<0.5
def test_validation_requires_evidence_for_exam():
    result=validate_result(AgentResult(agent=AgentName.EXAM,answer="x"))
    assert result.requires_human_review
