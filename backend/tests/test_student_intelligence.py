from app.student_intelligence.contracts import StudentOnboardingInput
from app.student_intelligence.profiler import build_profile
from app.student_intelligence.questions import next_questions


def test_profile_reports_missing_dimensions():
    profile = build_profile(
        StudentOnboardingInput(
            education_stage="AFTER_12",
            country_code="IN",
            interests=["technology"],
        )
    )
    assert profile.completeness_score > 0
    assert "budget" in profile.missing_dimensions
    assert next_questions(profile)
