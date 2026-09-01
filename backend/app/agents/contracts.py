from enum import StrEnum
from pydantic import BaseModel, Field


class AgentName(StrEnum):
    SUPERVISOR = "supervisor"
    CAREER = "career"
    ADMISSIONS = "admissions"
    SCHOLARSHIP = "scholarship"
    EXAM = "exam"
    RESEARCH = "research"
    RECOMMENDATION = "recommendation"


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    user_id: str
    conversation_id: str | None = None
    allowed_agents: list[AgentName] | None = None


class AgentResult(BaseModel):
    agent: AgentName
    answer: str
    actions: list[str] = Field(default_factory=list)
    evidence: list[dict] = Field(default_factory=list)
    requires_human_review: bool = False


class AgentPlan(BaseModel):
    primary_agent: AgentName
    supporting_agents: list[AgentName] = Field(default_factory=list)
    reason: str
