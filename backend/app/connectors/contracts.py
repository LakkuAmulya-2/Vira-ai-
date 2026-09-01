from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl

class ConnectorType(StrEnum):
    WEB = "WEB"
    API = "API"
    DOCUMENT = "DOCUMENT"

class ConnectorJobRequest(BaseModel):
    source_url: HttpUrl
    connector_type: ConnectorType = ConnectorType.WEB
    country_code: str | None = Field(default=None, max_length=2)
    jurisdiction: str | None = Field(default=None, max_length=160)
    entity_type: str = Field(default="education_source", max_length=80)
    dry_run: bool = True

class ConnectorJobResponse(BaseModel):
    job_id: str
    status: str
    source_url: str
    dry_run: bool
