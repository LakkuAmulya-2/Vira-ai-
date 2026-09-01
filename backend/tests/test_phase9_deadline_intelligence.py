from datetime import date,timedelta
from app.deadlines.contracts import DeadlineSignal
from app.deadlines.intelligence import assess
def test_deadline_priority():
 s=DeadlineSignal(entity_type="scholarship",entity_key="x",title="X",deadline=date.today()+timedelta(days=2))
 assert assess(s).priority=="CRITICAL"
def test_normal_deadline():
 s=DeadlineSignal(entity_type="exam",entity_key="x",title="X",deadline=date.today()+timedelta(days=30))
 assert assess(s).priority=="NORMAL"
