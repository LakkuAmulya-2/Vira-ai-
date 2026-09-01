from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.contracts import CandidateClaimInput
from app.knowledge.validation import validate_candidate_claim
from app.models.knowledge import DataSource, KnowledgeClaim

async def ingest_candidate_claim(db: AsyncSession, claim: CandidateClaimInput) -> dict:
    validate_candidate_claim(claim)
    source_url = str(claim.source_url).rstrip("/")
    source = await db.scalar(select(DataSource).where(DataSource.base_url == source_url))

    if source is None:
        source = DataSource(
            name=claim.source_url.host,
            base_url=source_url,
            source_type=claim.source_type.value,
            country_code=claim.country_code.upper() if claim.country_code else None,
            verification_status="PENDING",
        )
        db.add(source)
        await db.flush()

    knowledge_claim = KnowledgeClaim(
        entity_type=claim.entity_type,
        entity_key=claim.entity_key,
        field=claim.field,
        value=claim.value,
        source_id=source.id,
        country_code=claim.country_code.upper() if claim.country_code else None,
        status="PENDING",
    )
    db.add(knowledge_claim)
    await db.commit()
    await db.refresh(knowledge_claim)

    return {
        "claim_id": knowledge_claim.id,
        "entity_type": knowledge_claim.entity_type,
        "entity_key": knowledge_claim.entity_key,
        "field": knowledge_claim.field,
        "status": "PENDING_VERIFICATION",
        "source_url": source_url,
    }
