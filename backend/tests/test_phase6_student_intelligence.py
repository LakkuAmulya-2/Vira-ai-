from app.student_intelligence.contracts import StudentOnboardingInput,StudentConstraintInput
from app.student_intelligence.profiler import build_profile
from app.student_intelligence.scoring import readiness
def test_profile_completeness():
    profile=build_profile(StudentOnboardingInput(education_stage="AFTER_12",country_code="IN",interests=["math"],skills=["python"],career_goals=["engineering"],annual_budget_minor=100000))
    assert profile.completeness_score>0
def test_readiness_threshold():
    profile=build_profile(StudentOnboardingInput(education_stage="AFTER_12",country_code="IN",academic_records=[],interests=["science"],strengths=["analysis"],skills=["python"],career_goals=["engineering"],preferred_countries=["IN"],annual_budget_minor=1,constraints=[StudentConstraintInput(category="location",value="hyderabad",importance=5)]))
    assert readiness(profile)["ready_for_personalization"] is True
