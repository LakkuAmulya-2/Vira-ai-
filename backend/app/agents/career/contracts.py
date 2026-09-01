from typing import Literal
from pydantic import BaseModel, Field

class CareerSignal(BaseModel):
    title: str
    rationale: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[str] = Field(default_factory=list)

class CareerDiscoveryRequest(BaseModel):
    profile: dict
    mode: Literal["explore", "refine"] = "explore"

class CareerDiscoveryResponse(BaseModel):
    summary: str
    signals: list[CareerSignal]
    assumptions: list[str] = Field(default_factory=list)
    next_questions: list[str] = Field(default_factory=list)
