from datetime import date
from pydantic import BaseModel,Field
class DeadlineSignal(BaseModel):
    entity_type:str
    entity_key:str
    title:str
    deadline:date
    source_id:str|None=None
    source_url:str|None=None
    metadata:dict=Field(default_factory=dict)
class DeadlineAssessment(BaseModel):
    entity_type:str
    entity_key:str
    deadline:date
    days_remaining:int
    priority:str
    eligible:bool
    action:str
