from app.recommendations.contracts import RankedCandidate
def confidence(item:RankedCandidate)->float:
    return round(min(1,.35+.4*min(1,len(item.candidate.evidence)/3)+.25*min(1,len(item.reasons)/4)),4)
def tier(item:RankedCandidate)->str:
    return "STRONG_MATCH" if item.score>=.8 else "GOOD_MATCH" if item.score>=.6 else "EXPLORATORY"
