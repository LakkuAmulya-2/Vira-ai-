from pydantic import BaseModel, Field


class BackgroundJob(BaseModel):
    job_type: str = Field(min_length=1, max_length=120)
    payload: dict = Field(default_factory=dict)
    idempotency_key: str | None = None
