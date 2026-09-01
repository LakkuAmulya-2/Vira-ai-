from functools import lru_cache
from app.core.config import settings
from langgraph.checkpoint.memory import MemorySaver
@lru_cache
def get_checkpointer():
    if settings.app_env.lower() in {"production","staging"} and not settings.langgraph_checkpointer_url:
        raise RuntimeError("LANGGRAPH_CHECKPOINTER_URL is required outside development")
    return MemorySaver()
