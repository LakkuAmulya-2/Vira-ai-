from app.student_intelligence.contracts import (
    StudentIntelligenceProfile,
    StudentOnboardingInput,
)


PROFILE_VERSION = "v1.0.0"


def build_profile(payload: StudentOnboardingInput) -> StudentIntelligenceProfile:
    dimensions = {
        "academic_history": bool(payload.academic_records),
        "interests": bool(payload.interests),
        "strengths": bool(payload.strengths),
        "skills": bool(payload.skills),
        "career_goals": bool(payload.career_goals),
        "preferred_countries": bool(payload.preferred_countries),
        "budget": payload.annual_budget_minor is not None,
        "constraints": bool(payload.constraints),
    }
    missing = [name for name, present in dimensions.items() if not present]
    return StudentIntelligenceProfile(
        profile_version=PROFILE_VERSION,
        completeness_score=round(sum(dimensions.values()) / len(dimensions), 2),
        strengths=payload.strengths,
        interests=payload.interests,
        skills=payload.skills,
        goals=payload.career_goals,
        constraints=payload.constraints,
        missing_dimensions=missing,
    )
