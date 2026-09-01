from datetime import date,datetime
from pydantic import BaseModel,Field
class ApplicationCreate(BaseModel):
    entity_type:str=Field(min_length=2,max_length=64)
    entity_key:str=Field(min_length=1,max_length=240)
    title:str
    application_url:str|None=None
    deadline:date|None=None
    metadata_json:dict=Field(default_factory=dict)
class TaskCreate(BaseModel):
    task_type:str
    title:str
    due_at:datetime|None=None
    payload:dict=Field(default_factory=dict)
class DocumentCreate(BaseModel):
    document_type:str
    storage_key:str|None=None
class ApplicationStatusUpdate(BaseModel):
    status:str
