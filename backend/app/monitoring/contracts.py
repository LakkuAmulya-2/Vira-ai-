from datetime import datetime
from pydantic import BaseModel, Field


class FreshnessCheck(BaseModel):
    source_id: str
    checked_at: datetime
    changed: bool = False
    metadata: dict = Field(default_factory=dict)


class DeadlineWatch(BaseModel):
    user_id: str
    entity_key: str
    deadline_at: datetime
    category: str
