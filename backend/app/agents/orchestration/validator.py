from app.agents.contracts import AgentResult
def validate_result(result:AgentResult)->AgentResult:
    evidence=result.evidence or []
    if result.agent.value in {"admissions","scholarship","exam","recommendation"} and not evidence:
        result.requires_human_review=True
    return result
def confidence(results:list[AgentResult])->float:
    if not results:return 0.0
    supported=sum(1 for result in results if result.evidence)
    review=sum(1 for result in results if result.requires_human_review)
    return max(0.0,min(1.0,0.45+0.45*(supported/len(results))-0.2*(review/len(results))))
