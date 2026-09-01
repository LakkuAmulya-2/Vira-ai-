from app.applications.readiness import readiness
class X:
 def __init__(self,status):self.status=status
def test_readiness():
    r=readiness([X("DONE"),X("TODO")],[X("VERIFIED")])
    assert r["completed_items"]==2 and r["total_items"]==3 and not r["ready_to_submit"]
