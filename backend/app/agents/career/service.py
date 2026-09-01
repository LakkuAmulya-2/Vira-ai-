from app.agents.career.contracts import CareerDiscoveryRequest, CareerDiscoveryResponse, CareerSignal

def discover_careers(request: CareerDiscoveryRequest) -> CareerDiscoveryResponse:
    profile = request.profile
    interests = profile.get("interests", [])
    strengths = profile.get("strengths", [])
    skills = profile.get("skills", [])
    missing = profile.get("missing_dimensions", [])
    evidence = [*interests, *strengths, *skills]
    signals: list[CareerSignal] = []

    if interests or skills:
        themes = list(dict.fromkeys([*interests, *skills]))[:5]
        for theme in themes:
            signals.append(CareerSignal(
                title=f"Explore {theme}",
                rationale=f"This direction is suggested because it appears in the student's stated interests or skills.",
                confidence=0.45,
                evidence=[theme],
            ))

    summary = (
        "These are exploration signals, not final career predictions. "
        "Vira should refine them with verified career knowledge and additional student context."
    )
    questions = []
    if "career_goals" in missing:
        questions.append("What kind of problems would you enjoy solving for many years?")
    if "academic_history" in missing:
        questions.append("What subjects and academic results best represent your current strengths?")
    if "budget" in missing:
        questions.append("What financial constraints should we consider while evaluating pathways?")
    return CareerDiscoveryResponse(summary=summary, signals=signals, next_questions=questions)
