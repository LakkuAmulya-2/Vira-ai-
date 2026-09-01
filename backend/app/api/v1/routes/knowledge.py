from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import CurrentUser, require_admin
from app.db.session import get_db
from app.models.knowledge import DataSource, KnowledgeClaim

router = APIRouter()


class DataSourceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    base_url: str = Field(min_length=8, max_length=2048)
    source_type: str = Field(min_length=2, max_length=64)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    jurisdiction: str | None = Field(default=None, max_length=160)


@router.post("/sources", status_code=201)
async def create_source(
    payload: DataSourceCreate,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    source = DataSource(**payload.model_dump())
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return {"id": source.id, "status": source.verification_status}


@router.post("/claims/{claim_id}/verify")
async def verify_claim(
    claim_id: str,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    claim = await db.get(KnowledgeClaim, claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    claim.status = "VERIFIED"
    await db.commit()
    return {"id": claim.id, "status": claim.status}
