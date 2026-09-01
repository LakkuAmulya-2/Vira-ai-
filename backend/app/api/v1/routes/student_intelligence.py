from fastapi import APIRouter, Depends

from app.core.security import CurrentUser, get_current_user
from app.student_intelligence.contracts import StudentOnboardingInput
from app.student_intelligence.profiler import build_profile
from app.student_intelligence.questions import next_questions

router = APIRouter()


@router.post("/profile")
async def build_student_intelligence_profile(
    payload: StudentOnboardingInput,
    user: CurrentUser = Depends(get_current_user),
):
    profile = build_profile(payload)
    return {
        "user_id": user.id,
        "profile": profile.model_dump(),
        "next_questions": next_questions(profile),
    }
