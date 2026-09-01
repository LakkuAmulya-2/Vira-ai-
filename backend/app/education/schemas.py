from datetime import date
from pydantic import BaseModel, Field, HttpUrl

class CountryCreate(BaseModel):
    iso_code:str=Field(min_length=2,max_length=2)
    name:str=Field(min_length=2,max_length=120)
    region:str=Field(min_length=2,max_length=80)

class InstitutionCreate(BaseModel):
    canonical_name:str=Field(min_length=2,max_length=300)
    country_code:str=Field(min_length=2,max_length=2)
    official_url:HttpUrl|None=None
    institution_type:str=Field(min_length=2,max_length=80)

class CourseCreate(BaseModel):
    canonical_name:str=Field(min_length=2,max_length=300)
    field_of_study:str=Field(min_length=2,max_length=160)
    level:str=Field(min_length=2,max_length=80)

class ProgramCreate(BaseModel):
    institution_id:str
    course_id:str
    official_name:str=Field(min_length=2,max_length=400)
    duration_months:int|None=Field(default=None,gt=0,le=240)
    delivery_mode:str|None=None
    tuition:dict|None=None
    eligibility:dict|None=None
    official_url:HttpUrl|None=None

class ScholarshipCreate(BaseModel):
    canonical_name:str=Field(min_length=2,max_length=400)
    provider_name:str=Field(min_length=2,max_length=300)
    country_code:str|None=Field(default=None,min_length=2,max_length=2)
    amount:dict|None=None
    eligibility:dict|None=None
    application_url:HttpUrl|None=None
    deadline:date|None=None

class EntranceExamCreate(BaseModel):
    canonical_name:str=Field(min_length=2,max_length=240)
    country_code:str|None=Field(default=None,min_length=2,max_length=2)
    organizer:str|None=Field(default=None,max_length=300)
    official_url:HttpUrl|None=None
    requirements:dict|None=None
