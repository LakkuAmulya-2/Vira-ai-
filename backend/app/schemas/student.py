from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class InterestInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    weight: int = Field(default=1, ge=1, le=10)


class SkillInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    proficiency: int | None = Field(default=None, ge=1, le=5)


class GoalInput(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    priority: int = Field(default=1, ge=1, le=10)


class StudentProfileUpsert(BaseModel):
    date_of_birth: date | None = None
    gender: Literal["FEMALE", "MALE", "NON_BINARY", "PREFER_NOT_TO_SAY"] | None = None
    country_code: str = Field(min_length=2, max_length=2)
    state: str | None = Field(default=None, max_length=120)
    city: str | None = Field(default=None, max_length=120)
    education_stage: Literal["AFTER_10", "AFTER_12", "UNDERGRADUATE", "OTHER"]
    preferred_countries: list[str] = Field(default_factory=list, max_length=20)
    preferred_languages: list[str] = Field(default_factory=list, max_length=20)
    budget_currency: str | None = Field(default=None, min_length=3, max_length=3)
    annual_budget_minor: int | None = Field(default=None, ge=0)
    interests: list[InterestInput] = Field(default_factory=list, max_length=50)
    skills: list[SkillInput] = Field(default_factory=list, max_length=50)
    goals: list[GoalInput] = Field(default_factory=list, max_length=20)

    @field_validator("country_code", "preferred_countries", mode="after")
    @classmethod
    def upper_country(cls, value):
        if isinstance(value, list):
            return [item.upper() for item in value]
        return value.upper()


class StudentProfileResponse(BaseModel):
    id: str
    updated_at: str
