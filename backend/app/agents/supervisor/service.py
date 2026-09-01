from app.agents.career.contracts import CareerDiscoveryRequest
from app.agents.career.service import discover_careers
from app.agents.supervisor.contracts import SupervisorRequest, SupervisorResponse

CAREER_TERMS = {"career", "course", "future", "job", "profession", "interest", "passion", "what should i study"}

def route_request(request: SupervisorRequest) -> SupervisorResponse:
    message = request.message.lower()
    if any(term in message for term in CAREER_TERMS):
        result = discover_careers(CareerDiscoveryRequest(profile=request.profile))
        return SupervisorResponse(
            route="career",
            answer=result.summary,
            confidence=0.6 if result.signals else 0.25,
            data={"signals": [signal.model_dump() for signal in result.signals]},
            follow_up_questions=result.next_questions,
        )
    return SupervisorResponse(
        route="student_intelligence",
        answer="I need a little more context before routing this to a specialist agent.",
        confidence=0.35,
        follow_up_questions=["What decision are you trying to make?", "Which education stage are you currently in?"],
    )
