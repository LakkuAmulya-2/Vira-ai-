from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.knowledge.connectors.contracts import SourceRegistration, VerificationDecision
from app.knowledge.connectors.service import register_source, review_claim

router = APIRouter()

@router.post("/")
async def register_official_source(
    payload: SourceRegistration,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
):
    return await register_source(db, payload)

@router.post("/claims/review")
async def review_knowledge_claim(
    payload: VerificationDecision,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
):
    try:
        return await review_claim(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
