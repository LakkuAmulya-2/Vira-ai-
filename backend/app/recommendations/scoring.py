from app.models.student import StudentProfile
from app.recommendations.contracts import Candidate, RankedCandidate


def score_candidate(student: StudentProfile, candidate: Candidate) -> RankedCandidate:
    score = 0.0
    reasons: list[str] = []

    preferred = set(student.preferred_countries)
    if candidate.country_code and candidate.country_code in preferred:
        score += 0.30
        reasons.append("Matches preferred study destination")

    interests = {item.name.lower(): item.weight for item in student.interests}
    candidate_interests = {str(x).lower() for x in candidate.attributes.get("interests", [])}
    overlap = candidate_interests.intersection(interests)
    if overlap:
        score += min(0.35, sum(interests[item] for item in overlap) / 30)
        reasons.append("Matches declared interests")

    goals = {item.title.lower(): item.priority for item in student.goals}
    candidate_goals = {str(x).lower() for x in candidate.attributes.get("career_goals", [])}
    if candidate_goals.intersection(goals):
        score += 0.20
        reasons.append("Supports stated career goals")

    if student.annual_budget_minor and candidate.annual_cost_minor and candidate.currency == student.budget_currency:
        affordability = 1 - (candidate.annual_cost_minor / student.annual_budget_minor)
        if affordability >= 0:
            score += min(0.15, affordability * 0.15)
            reasons.append("Fits stated budget")

    return RankedCandidate(candidate=candidate, score=round(min(score, 1.0), 4), reasons=reasons)
