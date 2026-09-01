from app.agents.contracts import AgentRequest
from app.agents.runtime import AgentRuntime
from app.workflows.student_journey.contracts import (
    JourneyRequest,
    JourneyResult,
    JourneyStatus,
    JourneyStep,
)
from app.workflows.student_journey.state import StudentJourneyState


class StudentJourneyWorkflow:
    STEPS = (
        JourneyStep.PROFILE,
        JourneyStep.CAREER,
        JourneyStep.COURSE,
        JourneyStep.COLLEGE,
        JourneyStep.SCHOLARSHIP,
        JourneyStep.EXAM,
        JourneyStep.ELIGIBILITY,
        JourneyStep.BUDGET,
        JourneyStep.TIMELINE,
        JourneyStep.PLAN,
    )

    def __init__(self, runtime: AgentRuntime) -> None:
        self.runtime = runtime

    async def run(self, request: JourneyRequest) -> JourneyResult:
        state = StudentJourneyState(
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            status=JourneyStatus.RUNNING,
        )

        for step in self.STEPS:
            results = await self.runtime.execute(
                AgentRequest(
                    message=f"Execute student journey step: {step.value}",
                    user_id=request.user_id,
                    conversation_id=request.conversation_id,
                )
            )
            state.complete(step, {"agent_results": [result.model_dump(mode="json") for result in results]})
            state.current_step = step

        state.status = JourneyStatus.COMPLETED
        return JourneyResult(
            status=state.status,
            completed_steps=state.completed_steps,
            artifacts=state.artifacts,
        )
