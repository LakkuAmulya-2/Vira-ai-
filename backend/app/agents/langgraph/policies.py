from app.agents.contracts import AgentName
ALLOWED_TOOLS:dict[str,set[str]]={
 AgentName.CAREER.value:{"knowledge.search"},
 AgentName.ADMISSIONS.value:{"knowledge.search"},
 AgentName.SCHOLARSHIP.value:{"knowledge.search"},
 AgentName.RESEARCH.value:{"knowledge.search"},
 AgentName.RECOMMENDATION.value:{"knowledge.search"},
 AgentName.EXAM.value:{"knowledge.search"},
}
def assert_tool_allowed(agent:str,tool:str)->None:
    if tool not in ALLOWED_TOOLS.get(agent,set()):
        raise PermissionError(f"Tool {tool} is not permitted for agent {agent}")
