from datetime import datetime, timezone

from app.monitoring.contracts import DeadlineWatch


def due_within(watches: list[DeadlineWatch], hours: int) -> list[DeadlineWatch]:
    now = datetime.now(timezone.utc)
    cutoff = now.timestamp() + hours * 3600
    return [watch for watch in watches if now.timestamp() <= watch.deadline_at.timestamp() <= cutoff]
