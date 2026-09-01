from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.connectors.contracts import SourceRegistration, VerificationDecision
from app.models.knowledge import DataSource, KnowledgeClaim

async def register_source(db: AsyncSession, payload: SourceRegistration) -> DataSource:
    base_url = str(payload.base_url).rstrip("/")
    existing = await db.scalar(select(DataSource).where(DataSource.base_url == base_url))
    if existing:
        return existing
    source = DataSource(
        name=payload.name,
        base_url=base_url,
        source_type=payload.source_type.value,
        country_code=payload.country_code.upper() if payload.country_code else None,
        jurisdiction=payload.jurisdiction,
        verification_status="PENDING",
    )
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source

async def review_claim(db: AsyncSession, payload: VerificationDecision) -> KnowledgeClaim:
    claim = await db.get(KnowledgeClaim, payload.claim_id)
    if claim is None:
        raise ValueError("Knowledge claim not found")
    claim.status = "VERIFIED" if payload.approved else "REJECTED"
    claim.verified_at = datetime.now(timezone.utc) if payload.approved else None
    await db.commit()
    await db.refresh(claim)
    return claim
