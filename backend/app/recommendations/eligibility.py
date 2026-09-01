from app.models.student import StudentProfile
from app.recommendations.contracts import Candidate
def is_eligible(student:StudentProfile,candidate:Candidate)->bool:
    attrs=candidate.attributes or {}
    countries=attrs.get("eligible_countries")
    if countries and student.country_code and student.country_code not in countries:return False
    if student.annual_budget_minor and candidate.annual_cost_minor and candidate.annual_cost_minor>student.annual_budget_minor:return False
    return True
