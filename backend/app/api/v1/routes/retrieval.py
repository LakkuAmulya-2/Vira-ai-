from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CurrentUser,get_current_user,require_admin
from app.db.session import get_db
from app.retrieval.contracts import GroundedContextRequest,RetrievalRequest
from app.retrieval.indexer import index_verified_claims
from app.retrieval.service import grounded_context,hybrid_search

router=APIRouter()

@router.post("/search")
async def search(payload:RetrievalRequest,db:AsyncSession=Depends(get_db),user:CurrentUser=Depends(get_current_user)):
    return await hybrid_search(db,payload,user.id)

@router.post("/context")
async def context(payload:GroundedContextRequest,db:AsyncSession=Depends(get_db),user:CurrentUser=Depends(get_current_user)):
    return await grounded_context(db,payload,user.id)

@router.post("/index",status_code=202)
async def index(limit:int=1000,db:AsyncSession=Depends(get_db),_:CurrentUser=Depends(require_admin)):
    return {"indexed":await index_verified_claims(db,limit)}
