from urllib.parse import urlparse

def validate_source_url(base_url:str,allowed_paths:list[str],target_url:str)->None:
    base=urlparse(base_url); target=urlparse(target_url)
    if target.scheme!="https": raise ValueError("Only HTTPS source URLs are allowed")
    if target.netloc.lower()!=base.netloc.lower(): raise ValueError("Target URL host is not registered for this source")
    if allowed_paths and not any(target.path.startswith(p) for p in allowed_paths):
        raise ValueError("Target URL path is outside the approved source scope")

def normalize_country_code(value:str|None)->str|None:
    return value.upper() if value else None
