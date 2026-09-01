from pydantic import BaseModel, Field


class AcademicRecordInput(BaseModel):
    qualification: str = Field(min_length=1, max_length=120)
    board_or_system: str | None = None
    score: float | None = Field(default=None, ge=0)
    score_scale: float | None = Field(default=None, gt=0)
    graduation_year: int | None = Field(default=None, ge=1950, le=2100)


class StudentConstraintInput(BaseModel):
    category: str = Field(min_length=1, max_length=80)
    value: str = Field(min_length=1, max_length=500)
    importance: int = Field(default=3, ge=1, le=5)


class StudentOnboardingInput(BaseModel):
    education_stage: str
    country_code: str = Field(min_length=2, max_length=2)
    academic_records: list[AcademicRecordInput] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list, max_length=30)
    strengths: list[str] = Field(default_factory=list, max_length=30)
    skills: list[str] = Field(default_factory=list, max_length=50)
    career_goals: list[str] = Field(default_factory=list, max_length=20)
    preferred_countries: list[str] = Field(default_factory=list, max_length=20)
    constraints: list[StudentConstraintInput] = Field(default_factory=list, max_length=30)
    annual_budget_minor: int | None = Field(default=None, ge=0)
    budget_currency: str | None = Field(default=None, min_length=3, max_length=3)


class StudentIntelligenceProfile(BaseModel):
    profile_version: str
    completeness_score: float = Field(ge=0, le=1)
    strengths: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    constraints: list[StudentConstraintInput] = Field(default_factory=list)
    missing_dimensions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
