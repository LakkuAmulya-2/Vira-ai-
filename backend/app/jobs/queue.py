import json
from app.core.config import settings

async def enqueue_connector_job(message: dict) -> None:
    if not settings.redis_url:
        raise RuntimeError("REDIS_URL is required for asynchronous jobs")
    import redis.asyncio as redis
    client = redis.from_url(settings.redis_url, decode_responses=True)
    try:
        await client.lpush("vira:connector:jobs", json.dumps(message))
    finally:
        await client.aclose()
