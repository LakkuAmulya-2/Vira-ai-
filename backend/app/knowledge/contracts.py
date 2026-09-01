from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl


class SourceType(StrEnum):
    API = "API"
    WEB = "WEB"
    DOCUMENT = "DOCUMENT"


class CandidateClaimInput(BaseModel):
    entity_type: str = Field(min_length=1, max_length=80)
    entity_key: str = Field(min_length=1, max_length=255)
    field: str = Field(min_length=1, max_length=120)
    value: dict | str | int | float | bool | None
    country_code: str | None = Field(default=None, max_length=2)
    source_url: HttpUrl
    source_type: SourceType
