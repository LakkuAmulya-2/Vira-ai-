from enum import StrEnum
from pydantic import BaseModel, Field


class JourneyStatus(StrEnum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
    WAITING_FOR_REVIEW = "WAITING_FOR_REVIEW"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JourneyStep(StrEnum):
    PROFILE = "PROFILE"
    CAREER = "CAREER"
    COURSE = "COURSE"
    COLLEGE = "COLLEGE"
    SCHOLARSHIP = "SCHOLARSHIP"
    EXAM = "EXAM"
    ELIGIBILITY = "ELIGIBILITY"
    BUDGET = "BUDGET"
    TIMELINE = "TIMELINE"
    PLAN = "PLAN"


class JourneyRequest(BaseModel):
    user_id: str
    conversation_id: str | None = None
    resume: bool = True


class JourneyResult(BaseModel):
    status: JourneyStatus
    completed_steps: list[JourneyStep] = Field(default_factory=list)
    next_step: JourneyStep | None = None
    artifacts: dict = Field(default_factory=dict)
