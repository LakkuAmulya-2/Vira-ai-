from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.contracts import CandidateClaimInput
from app.knowledge.validation import validate_candidate_claim


async def ingest_candidate_claim(db: AsyncSession, claim: CandidateClaimInput) -> dict:
    validate_candidate_claim(claim)
    # Persistence is intentionally routed through the existing verified knowledge
    # domain. Candidate facts must remain pending until verification.
    return {
        "entity_type": claim.entity_type,
        "entity_key": claim.entity_key,
        "field": claim.field,
        "status": "PENDING_VERIFICATION",
        "source_url": str(claim.source_url),
    }
