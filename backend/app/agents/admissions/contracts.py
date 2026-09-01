from enum import StrEnum
from pydantic import BaseModel, Field

class ActionStatus(StrEnum):
    READY = "READY"
    BLOCKED = "BLOCKED"
    NEEDS_REVIEW = "NEEDS_REVIEW"

class AdmissionGoal(BaseModel):
    country_code: str | None = None
    target_intake: str | None = None
    intended_program: str | None = None

class JourneyAction(BaseModel):
    id: str
    title: str
    category: str
    status: ActionStatus
    depends_on: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)

class AdmissionsPlanRequest(BaseModel):
    profile: dict = Field(default_factory=dict)
    goal: AdmissionGoal = Field(default_factory=AdmissionGoal)

class AdmissionsPlanResponse(BaseModel):
    summary: str
    actions: list[JourneyAction]
    next_action: JourneyAction | None = None
    assumptions: list[str] = Field(default_factory=list)
