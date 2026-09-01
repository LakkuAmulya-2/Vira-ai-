from pydantic import BaseModel, Field

class ScholarshipCandidate(BaseModel):
    scholarship_id: str
    name: str
    country_code: str | None = None
    amount: float | None = None
    deadline: str | None = None
    eligibility: dict = Field(default_factory=dict)
    required_documents: list[str] = Field(default_factory=list)

class ScholarshipMatchRequest(BaseModel):
    profile: dict = Field(default_factory=dict)
    scholarships: list[ScholarshipCandidate] = Field(default_factory=list)

class ScholarshipMatch(BaseModel):
    scholarship_id: str
    name: str
    eligibility_score: float = Field(ge=0, le=100)
    status: str
    reasons: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)
    deadline: str | None = None

class ScholarshipMatchResponse(BaseModel):
    matches: list[ScholarshipMatch]
    assumptions: list[str] = Field(default_factory=list)
