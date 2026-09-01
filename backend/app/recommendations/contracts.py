from pydantic import BaseModel, Field


class Candidate(BaseModel):
    entity_type: str
    entity_key: str
    title: str
    country_code: str | None = None
    annual_cost_minor: int | None = None
    currency: str | None = None
    attributes: dict = Field(default_factory=dict)
    evidence: list[dict] = Field(default_factory=list)


class RankedCandidate(BaseModel):
    candidate: Candidate
    score: float = Field(ge=0, le=1)
    reasons: list[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    algorithm_version: str
    items: list[RankedCandidate]
