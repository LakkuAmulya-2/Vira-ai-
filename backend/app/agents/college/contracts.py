from enum import StrEnum
from pydantic import BaseModel, Field

class MatchBand(StrEnum):
    REACH = "REACH"
    MATCH = "MATCH"
    SAFE = "SAFE"
    UNKNOWN = "UNKNOWN"

class CollegeCandidate(BaseModel):
    college_id: str
    name: str
    country_code: str
    program: str | None = None
    tuition: float | None = None
    eligibility: dict = Field(default_factory=dict)

class CollegeMatchRequest(BaseModel):
    profile: dict = Field(default_factory=dict)
    candidates: list[CollegeCandidate] = Field(default_factory=list)

class CollegeMatch(BaseModel):
    college_id: str
    name: str
    band: MatchBand
    score: float = Field(ge=0, le=100)
    reasons: list[str]
    missing_information: list[str] = Field(default_factory=list)

class CollegeMatchResponse(BaseModel):
    matches: list[CollegeMatch]
    assumptions: list[str] = Field(default_factory=list)
