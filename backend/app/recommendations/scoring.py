from app.models.student import StudentProfile
from app.recommendations.contracts import Candidate,RankedCandidate
def score_candidate(student:StudentProfile,candidate:Candidate)->RankedCandidate:
    score=.25;reasons=[];attrs=candidate.attributes or {}
    if candidate.country_code and candidate.country_code in (student.preferred_countries or []):score+=.2;reasons.append("Matches preferred study country")
    if student.annual_budget_minor and candidate.annual_cost_minor:
        score+=.2*max(0,1-abs(1-candidate.annual_cost_minor/max(student.annual_budget_minor,1)));reasons.append("Fits the stated budget")
    interests={x.name.lower() for x in student.interests};tags={str(x).lower() for x in attrs.get("interests",[])}
    if interests&tags:score+=min(.25,.08*len(interests&tags));reasons.append("Matches your interests")
    goals={x.title.lower() for x in student.goals};goal_tags={str(x).lower() for x in attrs.get("career_goals",[])}
    if goals&goal_tags:score+=.2;reasons.append("Supports your career goals")
    if not reasons:reasons.append("Verified candidate; add more profile details for stronger personalization")
    return RankedCandidate(candidate=candidate,score=min(1,round(score,4)),reasons=reasons)
