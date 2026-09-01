from datetime import datetime, timezone
from pydantic import BaseModel, Field

from app.agents.contracts import AgentName


class AgentEvent(BaseModel):
    agent: AgentName
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict = Field(default_factory=dict)


class WorkflowState(BaseModel):
    conversation_id: str | None = None
    user_id: str
    step: int = 0
    events: list[AgentEvent] = Field(default_factory=list)
    requires_human_review: bool = False

    def add_event(self, event: AgentEvent) -> None:
        self.events.append(event)
        self.step += 1
