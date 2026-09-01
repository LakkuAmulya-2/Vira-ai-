from app.ai.contracts import AIProvider


def get_ai_provider() -> AIProvider:
    raise RuntimeError(
        "No AI provider configured. Configure an approved provider adapter through environment settings."
    )
