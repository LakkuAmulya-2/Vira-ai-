from enum import StrEnum
from pydantic import BaseModel, Field

class JobStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ConnectorJobMessage(BaseModel):
    job_id: str
    source_url: str
    connector_type: str
    country_code: str | None = Field(default=None, max_length=2)
    jurisdiction: str | None = None
    entity_type: str = "education_source"

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
