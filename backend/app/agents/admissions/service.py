from app.agents.admissions.contracts import AdmissionGoal, AdmissionsPlanRequest, AdmissionsPlanResponse, ActionStatus, JourneyAction

def _missing(profile: dict, keys: list[str]) -> list[str]:
    return [key for key in keys if profile.get(key) in (None, "", [], {})]

def _action(id: str, title: str, category: str, profile: dict, required: list[str], depends_on: list[str] | None = None) -> JourneyAction:
    missing = _missing(profile, required)
    return JourneyAction(
        id=id,
        title=title,
        category=category,
        status=ActionStatus.BLOCKED if missing else ActionStatus.READY,
        depends_on=depends_on or [],
        reasons=["Required context is available."] if not missing else ["More verified student context is required before this action can be automated."],
        missing_information=missing,
    )

def build_admissions_plan(request: AdmissionsPlanRequest) -> AdmissionsPlanResponse:
    profile = request.profile
    goal: AdmissionGoal = request.goal
    enriched = {**profile, "target_country": goal.country_code or profile.get("target_country"), "target_intake": goal.target_intake or profile.get("target_intake"), "intended_program": goal.intended_program or profile.get("intended_program")}

    actions = [
        _action("profile", "Complete student intelligence profile", "PROFILE", enriched, ["education_stage", "academics"]),
        _action("career", "Validate career direction", "CAREER", enriched, ["interests"], ["profile"]),
        _action("course", "Select course pathways", "COURSE", enriched, ["intended_program"], ["career"]),
        _action("college", "Build verified college shortlist", "COLLEGE", enriched, ["target_country", "academics", "budget"], ["course"]),
        _action("scholarship", "Check scholarship eligibility", "SCHOLARSHIP", enriched, ["target_country", "academics", "household_income"], ["college"]),
        _action("exams", "Check entrance and language requirements", "EXAM", enriched, ["target_country", "intended_program"], ["college"]),
        _action("documents", "Prepare application documents", "DOCUMENTS", enriched, ["full_name"], ["college"]),
        _action("applications", "Create application action queue", "APPLICATION", enriched, ["target_intake"], ["documents", "exams", "scholarship"]),
        _action("timeline", "Generate deadline timeline", "TIMELINE", enriched, ["target_intake", "target_country"], ["applications"]),
    ]
    next_action = next((item for item in actions if item.status == ActionStatus.READY), None)
    if next_action is None:
        next_action = next((item for item in actions if item.status == ActionStatus.BLOCKED), None)
    return AdmissionsPlanResponse(
        summary="This is an execution plan, not an admission guarantee. Official requirements and deadlines must be verified before action.",
        actions=actions,
        next_action=next_action,
        assumptions=["No application is submitted autonomously without explicit student authorization.", "Official sources remain the source of truth for eligibility and deadlines."],
    )
