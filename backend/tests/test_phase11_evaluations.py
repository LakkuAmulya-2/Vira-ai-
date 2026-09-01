from app.evaluations.contracts import EvaluationCase
from app.evaluations.copilot import evaluate
def test_evaluation():
 r=evaluate(EvaluationCase(name="career",query="help",expected_capabilities=["career"]),{"answer":"career guidance"})
 assert r.passed and r.score==1
