from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl

class ConnectorKind(StrEnum):
    OFFICIAL_WEB = "OFFICIAL_WEB"
    OFFICIAL_API = "OFFICIAL_API"
    DOCUMENT = "DOCUMENT"

class SourceRegistration(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    base_url: HttpUrl
    source_type: ConnectorKind
    country_code: str | None = Field(default=None, max_length=2)
    jurisdiction: str | None = Field(default=None, max_length=160)

class VerificationDecision(BaseModel):
    claim_id: str
    approved: bool
    reviewer_id: str | None = None
    reason: str = Field(min_length=3, max_length=1000)
