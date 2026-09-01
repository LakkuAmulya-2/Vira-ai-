from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser, get_current_user, require_admin
from app.db.session import get_db
from app.education import schemas
from app.education.service import create_entity, get_entity, search_entities
from app.models.education import Country, Institution, Course, Program, Scholarship, EntranceExam

router=APIRouter()

def admin(_:CurrentUser=Depends(require_admin)): return _

@router.post("/countries",status_code=201)
async def create_country(p:schemas.CountryCreate,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)): return await create_entity(db,Country,p.model_dump())
@router.post("/institutions",status_code=201)
async def create_institution(p:schemas.InstitutionCreate,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)): return await create_entity(db,Institution,{**p.model_dump(exclude={"official_url"}),"official_url":str(p.official_url) if p.official_url else None})
@router.post("/courses",status_code=201)
async def create_course(p:schemas.CourseCreate,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)): return await create_entity(db,Course,p.model_dump())
@router.post("/programs",status_code=201)
async def create_program(p:schemas.ProgramCreate,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)): return await create_entity(db,Program,{**p.model_dump(exclude={"official_url"}),"official_url":str(p.official_url) if p.official_url else None})
@router.post("/scholarships",status_code=201)
async def create_scholarship(p:schemas.ScholarshipCreate,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)): return await create_entity(db,Scholarship,{**p.model_dump(exclude={"application_url"}),"application_url":str(p.application_url) if p.application_url else None})
@router.post("/exams",status_code=201)
async def create_exam(p:schemas.EntranceExamCreate,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)): return await create_entity(db,EntranceExam,{**p.model_dump(exclude={"official_url"}),"official_url":str(p.official_url) if p.official_url else None})

@router.get("/institutions")
async def list_institutions(q:str|None=None,country_code:str|None=None,limit:int=20,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(get_current_user)): return await search_entities(db,Institution,q,country_code,limit)
@router.get("/courses")
async def list_courses(q:str|None=None,limit:int=20,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(get_current_user)): return await search_entities(db,Course,q,None,limit)
@router.get("/scholarships")
async def list_scholarships(q:str|None=None,country_code:str|None=None,limit:int=20,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(get_current_user)): return await search_entities(db,Scholarship,q,country_code,limit)
