from app.recommendations.contracts import Candidate
from app.recommendations.decision import confidence,tier
from app.recommendations.scoring import score_candidate
from app.models.student import StudentProfile
def test_decision_confidence_and_tier():
    candidate=Candidate(entity_type="course",entity_key="x",title="X",evidence=[{"source_id":"1"}])
    class S: interests=[];goals=[];preferred_countries=[];annual_budget_minor=None
    item=score_candidate(S(),candidate);item.confidence=confidence(item);item.tier=tier(item)
    assert 0<=item.confidence<=1
    assert item.tier in {"STRONG_MATCH","GOOD_MATCH","EXPLORATORY"}
