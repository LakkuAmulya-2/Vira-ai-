from app.student_intelligence.contracts import (
    StudentIntelligenceProfile,
    StudentOnboardingInput,
)
from app.student_intelligence.profiler import build_profile


def create_intelligence_profile(
    payload: StudentOnboardingInput,
) -> StudentIntelligenceProfile:
    return build_profile(payload)
