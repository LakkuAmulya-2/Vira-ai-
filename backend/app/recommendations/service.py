from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge import KnowledgeClaim
from app.models.student import StudentProfile
from app.models.recommendation import RecommendationRun,RecommendationItem
from app.recommendations.contracts import Candidate,RecommendationResponse
from app.recommendations.eligibility import is_eligible
from app.recommendations.scoring import score_candidate
from app.recommendations.decision import confidence,tier
ALGORITHM_VERSION="v2.0.0"
async def recommend(db:AsyncSession,student:StudentProfile,*,entity_type:str,limit:int=20)->RecommendationResponse:
    result=await db.execute(select(KnowledgeClaim).where(KnowledgeClaim.entity_type==entity_type,KnowledgeClaim.field=="profile",KnowledgeClaim.status=="VERIFIED"))
    candidates=[]
    for claim in result.scalars():
        value=claim.value if isinstance(claim.value,dict) else {}
        candidates.append(Candidate(entity_type=entity_type,entity_key=claim.entity_key,title=str(value.get("title",claim.entity_key)),country_code=claim.country_code,annual_cost_minor=value.get("annual_cost_minor"),currency=value.get("currency"),attributes=value.get("attributes",{}),evidence=[{"claim_id":claim.id,"source_id":claim.source_id}]))
    ranked=[]
    for candidate in candidates:
        if not is_eligible(student,candidate):continue
        item=score_candidate(student,candidate);item.confidence=confidence(item);item.tier=tier(item);ranked.append(item)
    ranked.sort(key=lambda x:(x.score,x.confidence),reverse=True);items=ranked[:limit]
    run=RecommendationRun(student_id=student.id,status="GENERATED",algorithm_version=ALGORITHM_VERSION,input_snapshot={"entity_type":entity_type,"limit":limit})
    db.add(run);await db.flush()
    db.add_all([RecommendationItem(run_id=run.id,entity_type=x.candidate.entity_type,entity_key=x.candidate.entity_key,score=x.score,reasons=x.reasons,evidence=x.candidate.evidence) for x in items]);await db.commit()
    return RecommendationResponse(algorithm_version=ALGORITHM_VERSION,items=items,generated_for_student_id=student.id)
