from app.agents.runtime.contracts import AgentName, AgentTask

CAREER_TERMS = {
    "career", "course", "future", "job", "profession", "interest",
    "passion", "study", "degree", "field", "stream"
}

def plan(message: str) -> list[AgentTask]:
    normalized = message.lower()
    tasks: list[AgentTask] = []

    if any(term in normalized for term in CAREER_TERMS):
        tasks.append(AgentTask(agent=AgentName.CAREER, reason="Career exploration intent detected", priority=10))

    if not tasks:
        tasks.append(AgentTask(agent=AgentName.STUDENT_INTELLIGENCE, reason="Clarify student decision context", priority=5))

    return tasks
