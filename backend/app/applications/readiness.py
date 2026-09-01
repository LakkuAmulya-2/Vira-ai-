from app.models.application import ApplicationDocument,ApplicationTask
def readiness(tasks:list[ApplicationTask],documents:list[ApplicationDocument])->dict:
    total=len(tasks)+len(documents)
    done=sum(x.status=="DONE" for x in tasks)+sum(x.status in {"READY","VERIFIED"} for x in documents)
    return {"total_items":total,"completed_items":done,"completion_score":round(done/total,4) if total else 0.0,"ready_to_submit":total>0 and done==total}
