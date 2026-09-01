from datetime import date
from pydantic import BaseModel, Field


class TimelineItem(BaseModel):
    title: str
    due_date: date | None = None
    category: str
    priority: int = Field(ge=1, le=5)
    source_claim_ids: list[str] = Field(default_factory=list)


def build_timeline(items: list[TimelineItem]) -> list[TimelineItem]:
    return sorted(items, key=lambda item: (item.due_date is None, item.due_date or date.max, -item.priority))
