from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl

class Region(StrEnum):
    INDIA="INDIA"
    US="US"
    UK="UK"
    EU="EU"
    GULF="GULF"

class SourceCategory(StrEnum):
    UNIVERSITY="UNIVERSITY"
    GOVERNMENT="GOVERNMENT"
    SCHOLARSHIP="SCHOLARSHIP"
    EXAM="EXAM"
    REGULATOR="REGULATOR"

class SourceProfileCreate(BaseModel):
    name:str=Field(min_length=2,max_length=200)
    base_url:HttpUrl
    region:Region
    country_code:str|None=Field(default=None,min_length=2,max_length=2)
    category:SourceCategory
    entity_type:str=Field(min_length=2,max_length=64)
    adapter_key:str=Field(min_length=2,max_length=64)
    allowed_paths:list[str]=Field(default_factory=list)
    crawl_interval_seconds:int=Field(default=86400,ge=300,le=2592000)
    enabled:bool=True

class SourceRunRequest(BaseModel):
    source_profile_id:str
    url:HttpUrl
    force:bool=False

class SourceRunResponse(BaseModel):
    job_id:str
    status:str
    adapter_key:str
