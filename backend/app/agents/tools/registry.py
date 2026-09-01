from collections.abc import Awaitable, Callable
from typing import Any

ToolHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        if name in self._tools:
            raise ValueError(f"Duplicate tool registration: {name}")
        self._tools[name] = handler

    async def invoke(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        handler = self._tools.get(name)
        if handler is None:
            raise PermissionError(f"Tool not allowlisted: {name}")
        return await handler(payload)

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)
