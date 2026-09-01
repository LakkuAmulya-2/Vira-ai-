from app.agents.runtime.supervisor import orchestrate
from app.agents.supervisor.contracts import SupervisorRequest, SupervisorResponse

def route_request(request: SupervisorRequest) -> SupervisorResponse:
    result = orchestrate(request.message, request.profile)
    return SupervisorResponse(
        route=result.route.value,
        answer=result.answer,
        confidence=result.confidence,
        data={**result.data, "execution_trace": [item.model_dump() for item in result.trace]},
        follow_up_questions=result.follow_up_questions,
    )
