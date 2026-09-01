from pydantic import BaseModel,Field
class AlertCreate(BaseModel):
    alert_type:str
    entity_type:str|None=None
    entity_key:str|None=None
    priority:str="NORMAL"
    title:str
    body:str
    action_url:str|None=None
    payload:dict=Field(default_factory=dict)
    dedupe_key:str
class NotificationPreferenceInput(BaseModel):
    deadline_alerts:bool=True
    scholarship_alerts:bool=True
    admission_alerts:bool=True
    exam_alerts:bool=True
    channels:dict=Field(default_factory=lambda:{"in_app":True})
    quiet_hours:dict=Field(default_factory=dict)
