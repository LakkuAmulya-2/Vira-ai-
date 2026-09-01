from typing import Literal
from pydantic import BaseModel, Field

AgentName = Literal["career", "student_intelligence", "knowledge"]

class SupervisorRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    profile: dict = Field(default_factory=dict)

class SupervisorResponse(BaseModel):
    route: AgentName
    answer: str
    confidence: float = Field(ge=0, le=1)
    data: dict = Field(default_factory=dict)
    follow_up_questions: list[str] = Field(default_factory=list)
