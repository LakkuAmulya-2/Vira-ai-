import time
from collections import defaultdict,deque
from fastapi import HTTPException,Request,status
from app.core.config import settings
_windows=defaultdict(deque)
async def rate_limit(request:Request):
    key=request.headers.get("x-forwarded-for",request.client.host if request.client else "unknown")
    now=time.monotonic();bucket=_windows[key];cutoff=now-60
    while bucket and bucket[0]<cutoff:bucket.popleft()
    if len(bucket)>=settings.rate_limit_per_minute:raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Rate limit exceeded")
    bucket.append(now)
