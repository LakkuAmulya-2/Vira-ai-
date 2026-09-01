from types import SimpleNamespace

from app.recommendations.contracts import Candidate
from app.recommendations.eligibility import is_eligible
from app.recommendations.scoring import score_candidate


def student():
    return SimpleNamespace(
        education_stage="AFTER_12",
        country_code="IN",
        annual_budget_minor=500000,
        budget_currency="INR",
        preferred_countries=["IN", "DE"],
        interests=[SimpleNamespace(name="computer science", weight=10)],
        goals=[SimpleNamespace(title="software engineer", priority=10)],
    )


def test_eligibility_and_scoring():
    candidate = Candidate(
        entity_type="course",
        entity_key="cs",
        title="Computer Science",
        country_code="DE",
        annual_cost_minor=200000,
        currency="INR",
        attributes={
            "education_stages": ["AFTER_12"],
            "eligible_countries": ["IN"],
            "interests": ["computer science"],
            "career_goals": ["software engineer"],
        },
    )
    assert is_eligible(student(), candidate)
    assert score_candidate(student(), candidate).score > 0
