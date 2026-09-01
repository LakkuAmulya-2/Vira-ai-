from app.agents.career.contracts import CareerDiscoveryRequest
from app.agents.career.service import discover_careers
from app.agents.runtime.contracts import AgentName, ExecutionTrace, OrchestrationResult
from app.agents.runtime.planner import plan
from app.agents.runtime.registry import AgentRegistry

def _career_handler(payload: dict) -> dict:
    result = discover_careers(CareerDiscoveryRequest(profile=payload.get("profile", {})))
    return {
        "answer": result.summary,
        "confidence": 0.6 if result.signals else 0.25,
        "data": {"signals": [signal.model_dump() for signal in result.signals]},
        "follow_up_questions": result.next_questions,
    }

def _student_intelligence_handler(payload: dict) -> dict:
    return {
        "answer": "I need a little more context before selecting a specialist agent.",
        "confidence": 0.35,
        "data": {},
        "follow_up_questions": [
            "What decision are you trying to make?",
            "Which education stage are you currently in?"
        ],
    }

def build_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(AgentName.CAREER, _career_handler)
    registry.register(AgentName.STUDENT_INTELLIGENCE, _student_intelligence_handler)
    return registry

def orchestrate(message: str, profile: dict) -> OrchestrationResult:
    tasks = sorted(plan(message), key=lambda task: task.priority, reverse=True)
    registry = build_registry()
    trace = [ExecutionTrace(agent=task.agent, status="planned", detail=task.reason) for task in tasks]

    primary = tasks[0]
    trace.append(ExecutionTrace(agent=primary.agent, status="running", detail="Executing specialist agent"))
    output = registry.execute(primary.agent, {"message": message, "profile": profile})
    trace.append(ExecutionTrace(agent=primary.agent, status="completed", detail="Specialist response aggregated"))

    return OrchestrationResult(
        route=primary.agent,
        answer=output["answer"],
        confidence=output["confidence"],
        data=output["data"],
        follow_up_questions=output["follow_up_questions"],
        trace=trace,
    )
