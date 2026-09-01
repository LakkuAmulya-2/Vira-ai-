from app.agents.college.contracts import CollegeCandidate, CollegeMatch, CollegeMatchRequest, CollegeMatchResponse, MatchBand

def _score(candidate: CollegeCandidate, profile: dict) -> CollegeMatch:
    reasons: list[str] = []
    missing: list[str] = []
    score = 50.0
    preferred = {str(x).upper() for x in profile.get("preferred_countries", [])}
    budget = profile.get("budget")
    academics = profile.get("academics", {})

    if preferred:
        if candidate.country_code.upper() in preferred:
            score += 15
            reasons.append("Matches a preferred destination.")
        else:
            score -= 10
            reasons.append("Outside the currently preferred destinations.")
    else:
        missing.append("preferred_countries")

    if budget is not None and candidate.tuition is not None:
        if candidate.tuition <= float(budget):
            score += 15
            reasons.append("Published tuition fits the stated budget.")
        else:
            score -= 20
            reasons.append("Published tuition exceeds the stated budget.")
    elif budget is None:
        missing.append("budget")

    minimum_score = candidate.eligibility.get("minimum_score")
    student_score = academics.get("score")
    if minimum_score is not None and student_score is not None:
        if float(student_score) >= float(minimum_score):
            score += 15
            reasons.append("Student score meets the supplied minimum threshold.")
        else:
            score -= 25
            reasons.append("Student score is below the supplied minimum threshold.")
    else:
        missing.append("academic_score_or_verified_threshold")

    score = max(0, min(100, score))
    band = MatchBand.UNKNOWN
    if not missing:
        band = MatchBand.REACH if score < 50 else MatchBand.MATCH if score < 75 else MatchBand.SAFE
    return CollegeMatch(college_id=candidate.college_id, name=candidate.name, band=band, score=score, reasons=reasons, missing_information=missing)

def match_colleges(request: CollegeMatchRequest) -> CollegeMatchResponse:
    matches = sorted((_score(candidate, request.profile) for candidate in request.candidates), key=lambda item: item.score, reverse=True)
    return CollegeMatchResponse(matches=matches, assumptions=["Scores are explainable heuristics; admission probability is never guaranteed."])
