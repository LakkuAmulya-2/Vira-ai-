from enum import Enum
from pydantic import BaseModel, Field

class AgentName(str, Enum):
    CAREER = "career"
    STUDENT_INTELLIGENCE = "student_intelligence"
    KNOWLEDGE = "knowledge"

class AgentTask(BaseModel):
    agent: AgentName
    reason: str
    priority: int = Field(ge=1, le=10)

class ExecutionTrace(BaseModel):
    agent: AgentName
    status: str
    detail: str

class OrchestrationResult(BaseModel):
    route: AgentName
    answer: str
    confidence: float = Field(ge=0, le=1)
    data: dict = Field(default_factory=dict)
    follow_up_questions: list[str] = Field(default_factory=list)
    trace: list[ExecutionTrace] = Field(default_factory=list)
