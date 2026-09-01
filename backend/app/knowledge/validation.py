from app.knowledge.contracts import CandidateClaimInput


def validate_candidate_claim(claim: CandidateClaimInput) -> None:
    if claim.value is None:
        raise ValueError("Knowledge claim value cannot be null")
    if claim.entity_type in {"college", "course", "scholarship", "exam"} and not claim.country_code:
        raise ValueError("country_code is required for this knowledge entity")
