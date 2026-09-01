import asyncio
from collections.abc import Awaitable,Callable
async def with_retry(operation:Callable[[],Awaitable],attempts:int=3,base_delay:float=0.25):
    error=None
    for attempt in range(attempts):
        try:return await operation()
        except Exception as exc:
            error=exc
            if attempt+1<attempts:await asyncio.sleep(base_delay*(2**attempt))
    raise error
