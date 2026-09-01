from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser,require_admin
from app.db.session import get_db
from app.ingestion.contracts import IngestionRequest
from app.ingestion.service import ingest_content

router=APIRouter()

@router.post("/content")
async def ingest(payload:IngestionRequest,content:str,content_type:str|None=None,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)):
    try:return await ingest_content(db,payload,content,content_type)
    except ValueError as exc:raise HTTPException(status_code=422,detail=str(exc)) from exc
