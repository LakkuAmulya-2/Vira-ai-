from pydantic import BaseModel, Field

class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    entity_type: str | None = None
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    jurisdiction: str | None = None
    limit: int = Field(default=10, ge=1, le=50)

class KnowledgeEvidence(BaseModel):
    claim_id: str
    entity_type: str
    entity_key: str
    field: str
    value: object
    source_name: str
    source_url: str
    country_code: str | None = None
    jurisdiction: str | None = None

class KnowledgeSearchResponse(BaseModel):
    query: str
    evidence: list[KnowledgeEvidence]
    total: int
