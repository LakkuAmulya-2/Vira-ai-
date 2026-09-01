from app.agents.scholarship.contracts import ScholarshipCandidate, ScholarshipMatch, ScholarshipMatchRequest, ScholarshipMatchResponse

def _evaluate(candidate: ScholarshipCandidate, profile: dict) -> ScholarshipMatch:
    score = 50.0
    reasons: list[str] = []
    missing: list[str] = []
    eligibility = candidate.eligibility

    country = profile.get("country_code")
    allowed_countries = {str(x).upper() for x in eligibility.get("countries", [])}
    if allowed_countries:
        if country:
            if country.upper() in allowed_countries:
                score += 15; reasons.append("Country eligibility matches the student profile.")
            else:
                score -= 35; reasons.append("Country does not match the supplied eligibility rule.")
        else: missing.append("country_code")

    student_score = profile.get("academics", {}).get("score")
    minimum_score = eligibility.get("minimum_score")
    if minimum_score is not None:
        if student_score is None: missing.append("academic_score")
        elif float(student_score) >= float(minimum_score):
            score += 15; reasons.append("Academic threshold is met.")
        else:
            score -= 25; reasons.append("Academic threshold is not currently met.")

    income = profile.get("household_income")
    maximum_income = eligibility.get("maximum_income")
    if maximum_income is not None:
        if income is None: missing.append("household_income")
        elif float(income) <= float(maximum_income):
            score += 15; reasons.append("Income requirement is met.")
        else:
            score -= 20; reasons.append("Income exceeds the supplied threshold.")

    status = "UNKNOWN" if missing else ("LIKELY_ELIGIBLE" if score >= 65 else "REVIEW_REQUIRED")
    return ScholarshipMatch(
        scholarship_id=candidate.scholarship_id,
        name=candidate.name,
        eligibility_score=max(0, min(100, score)),
        status=status,
        reasons=reasons,
        missing_information=missing,
        required_documents=candidate.required_documents,
        deadline=candidate.deadline,
    )

def match_scholarships(request: ScholarshipMatchRequest) -> ScholarshipMatchResponse:
    matches = sorted((_evaluate(item, request.profile) for item in request.scholarships), key=lambda item: item.eligibility_score, reverse=True)
    return ScholarshipMatchResponse(
        matches=matches,
        assumptions=["Eligibility results are preliminary. Students must verify final requirements with the official scholarship provider."]
    )
