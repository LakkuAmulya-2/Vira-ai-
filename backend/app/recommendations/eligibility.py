from app.models.student import StudentProfile
from app.recommendations.contracts import Candidate


def is_eligible(student: StudentProfile, candidate: Candidate) -> bool:
    stages = candidate.attributes.get("education_stages")
    if stages and student.education_stage not in stages:
        return False

    countries = candidate.attributes.get("eligible_countries")
    if countries and student.country_code not in countries:
        return False

    if (
        student.annual_budget_minor is not None
        and candidate.annual_cost_minor is not None
        and candidate.currency == student.budget_currency
        and candidate.annual_cost_minor > student.annual_budget_minor
    ):
        return False

    return True
