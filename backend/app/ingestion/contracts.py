from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl

class IngestionMode(StrEnum):
    FETCH="FETCH"
    DOCUMENT="DOCUMENT"

class IngestionRequest(BaseModel):
    source_id:str
    url:HttpUrl
    mode:IngestionMode=IngestionMode.FETCH
    country_code:str|None=Field(default=None,min_length=2,max_length=2)
    entity_type:str|None=Field(default=None,max_length=64)
    force:bool=False

class IngestionResult(BaseModel):
    document_id:str
    changed:bool
    status:str
    extracted_claims:int
