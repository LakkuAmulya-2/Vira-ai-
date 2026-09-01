import pytest
from pydantic import ValidationError

from app.knowledge.contracts import CandidateClaimInput, SourceType
from app.knowledge.validation import validate_candidate_claim


def test_rejects_missing_country_for_college():
    claim = CandidateClaimInput(
        entity_type="college",
        entity_key="example",
        field="profile",
        value={"title": "Example"},
        source_url="https://example.org/source",
        source_type=SourceType.WEB,
    )
    with pytest.raises(ValueError):
        validate_candidate_claim(claim)
