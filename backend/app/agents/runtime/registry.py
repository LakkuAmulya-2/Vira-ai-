from collections.abc import Callable
from typing import Any
from app.agents.runtime.contracts import AgentName

AgentHandler = Callable[[dict[str, Any]], dict[str, Any]]

class AgentRegistry:
    def __init__(self) -> None:
        self._handlers: dict[AgentName, AgentHandler] = {}

    def register(self, name: AgentName, handler: AgentHandler) -> None:
        self._handlers[name] = handler

    def execute(self, name: AgentName, payload: dict[str, Any]) -> dict[str, Any]:
        handler = self._handlers.get(name)
        if handler is None:
            raise ValueError(f"Agent '{name.value}' is not registered")
        return handler(payload)
