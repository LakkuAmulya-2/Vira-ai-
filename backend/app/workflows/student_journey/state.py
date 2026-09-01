from pydantic import BaseModel, Field

from app.workflows.student_journey.contracts import JourneyStatus, JourneyStep


class StudentJourneyState(BaseModel):
    user_id: str
    conversation_id: str | None = None
    status: JourneyStatus = JourneyStatus.CREATED
    current_step: JourneyStep = JourneyStep.PROFILE
    completed_steps: list[JourneyStep] = Field(default_factory=list)
    artifacts: dict = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)

    def complete(self, step: JourneyStep, artifact: dict) -> None:
        if step not in self.completed_steps:
            self.completed_steps.append(step)
        self.artifacts[step.value.lower()] = artifact
