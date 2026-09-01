import hashlib


def workflow_key(user_id: str, workflow_type: str, request_key: str) -> str:
    value = f"{user_id}:{workflow_type}:{request_key}".encode()
    return hashlib.sha256(value).hexdigest()
