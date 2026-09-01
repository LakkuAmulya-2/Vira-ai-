from datetime import datetime, timedelta, timezone

from app.monitoring.contracts import DeadlineWatch
from app.monitoring.service import due_within


def test_deadline_window():
    watch = DeadlineWatch(
        user_id="u1",
        entity_key="scholarship-1",
        deadline_at=datetime.now(timezone.utc) + timedelta(hours=12),
        category="scholarship",
    )
    assert due_within([watch], 24) == [watch]
