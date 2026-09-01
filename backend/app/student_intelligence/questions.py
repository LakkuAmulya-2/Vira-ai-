from app.student_intelligence.contracts import StudentIntelligenceProfile


def next_questions(profile: StudentIntelligenceProfile, limit: int = 3) -> list[str]:
    prompts = {
        "academic_history": "Tell us your latest qualification, board/system, and score.",
        "interests": "Which subjects or activities genuinely interest you?",
        "strengths": "What do you believe you are naturally good at?",
        "skills": "Which skills have you already developed?",
        "career_goals": "What kind of problems or careers would you like to explore?",
        "preferred_countries": "Which countries are you open to studying in?",
        "budget": "What annual education budget range is comfortable for your family?",
        "constraints": "Are there location, financial, family, health, or other constraints we should respect?",
    }
    return [prompts[key] for key in profile.missing_dimensions[:limit]]
