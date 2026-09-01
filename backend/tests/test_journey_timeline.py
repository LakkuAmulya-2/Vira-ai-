from datetime import date

from app.workflows.student_journey.timeline import TimelineItem, build_timeline


def test_timeline_orders_due_dates():
    items = [
        TimelineItem(title="Later", due_date=date(2027, 2, 1), category="application", priority=3),
        TimelineItem(title="Sooner", due_date=date(2026, 12, 1), category="exam", priority=2),
    ]
    assert build_timeline(items)[0].title == "Sooner"
