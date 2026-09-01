from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import KnowledgeClaim
from app.models.student import StudentProfile
from app.recommendations.contracts import Candidate, RecommendationResponse
from app.recommendations.eligibility import is_eligible
from app.recommendations.scoring import score_candidate

ALGORITHM_VERSION = "v1.0.0"


async def recommend(
    db: AsyncSession,
    student: StudentProfile,
    *,
    entity_type: str,
    limit: int = 20,
) -> RecommendationResponse:
    result = await db.execute(
        select(KnowledgeClaim).where(
            KnowledgeClaim.entity_type == entity_type,
            KnowledgeClaim.field == "profile",
            KnowledgeClaim.status == "VERIFIED",
        )
    )

    candidates: list[Candidate] = []
    for claim in result.scalars():
        value = claim.value if isinstance(claim.value, dict) else {}
        candidates.append(
            Candidate(
                entity_type=entity_type,
                entity_key=claim.entity_key,
                title=str(value.get("title", claim.entity_key)),
                country_code=claim.country_code,
                annual_cost_minor=value.get("annual_cost_minor"),
                currency=value.get("currency"),
                attributes=value.get("attributes", {}),
                evidence=[{"claim_id": claim.id, "source_id": claim.source_id}],
            )
        )

    ranked = [
        score_candidate(student, candidate)
        for candidate in candidates
        if is_eligible(student, candidate)
    ]
    ranked.sort(key=lambda item: item.score, reverse=True)
    return RecommendationResponse(algorithm_version=ALGORITHM_VERSION, items=ranked[:limit])
