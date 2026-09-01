from app.student_intelligence.contracts import StudentIntelligenceProfile

def readiness(profile:StudentIntelligenceProfile)->dict:
    return {"completeness":profile.completeness_score,"ready_for_personalization":profile.completeness_score>=0.6,"priority_dimensions":profile.missing_dimensions[:3]}

def constraint_summary(context:dict)->dict:
    hard=[x for x in context.get("constraints",[]) if x.get("importance",0)>=4]
    return {"hard_constraints":hard,"budget_minor":context.get("annual_budget_minor"),"preferred_countries":context.get("preferred_countries",[])}
