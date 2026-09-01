from app.recommendations.contracts import RankedCandidate
def explain(item:RankedCandidate)->dict:
    return {"entity_key":item.candidate.entity_key,"score":item.score,"confidence":item.confidence,"tier":item.tier,"reasons":item.reasons,"evidence":item.candidate.evidence,"limitations":["Recommendations are decision support, not guaranteed admissions or funding outcomes"]}
