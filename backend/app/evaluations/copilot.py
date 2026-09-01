from app.evaluations.contracts import EvaluationCase,EvaluationResult
def evaluate(case:EvaluationCase,response:dict)->EvaluationResult:
    text=str(response).lower();hits=sum(1 for capability in case.expected_capabilities if capability.lower() in text)
    score=hits/max(1,len(case.expected_capabilities))
    return EvaluationResult(name=case.name,passed=score>=0.5,score=score,details={"matched":hits})
