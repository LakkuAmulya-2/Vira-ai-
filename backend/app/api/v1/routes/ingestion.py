from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, get_current_user
from app.db.session import get_db
from app.knowledge.contracts import CandidateClaimInput
from app.knowledge.ingestion import ingest_candidate_claim

router = APIRouter()


@router.post("/claims")
async def submit_candidate_claim(
    payload: CandidateClaimInput,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    # Role checks should be enforced by the production identity provider boundary.
    try:
        return await ingest_candidate_claim(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
