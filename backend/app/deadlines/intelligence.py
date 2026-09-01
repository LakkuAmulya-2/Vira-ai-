from datetime import date
from app.deadlines.contracts import DeadlineSignal,DeadlineAssessment
def assess(signal:DeadlineSignal,eligible:bool=True,today:date|None=None)->DeadlineAssessment:
    today=today or date.today();days=(signal.deadline-today).days
    priority="CRITICAL" if days<=3 else "HIGH" if days<=14 else "NORMAL"
    action="Review immediately" if days<=3 else "Prepare required documents" if days<=14 else "Track and plan"
    return DeadlineAssessment(entity_type=signal.entity_type,entity_key=signal.entity_key,deadline=signal.deadline,days_remaining=days,priority=priority,eligible=eligible,action=action)
