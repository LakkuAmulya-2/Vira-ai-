from collections.abc import AsyncIterator
from typing import Any
async def stream_events(graph,initial:dict,config:dict)->AsyncIterator[dict[str,Any]]:
    async for event in graph.astream(initial,config=config,stream_mode="updates"):
        yield event
