import pytest
from app.source_intelligence.policies import validate_source_url
from app.source_intelligence.adapters import get_adapter
from app.source_intelligence.adapters.base import AdapterContext
def test_rejects_unregistered_host():
    with pytest.raises(ValueError):validate_source_url("https://example.edu",[],"https://evil.example/path")
def test_rejects_http():
    with pytest.raises(ValueError):validate_source_url("https://example.edu",[],"http://example.edu/path")
def test_allowed_path():
    validate_source_url("https://example.edu",["/admissions"],"https://example.edu/admissions/page")
def test_india_adapter_extracts_jsonld():
    adapter=get_adapter("india_official")
    _,claims=adapter.extract('<html><head><script type="application/ld+json">{"@type":"College","name":"Real Name"}</script></head></html>',"text/html",AdapterContext("INDIA","IN","UNIVERSITY","institution"))
    assert any(c.entity_key=="Real Name" for c in claims)
def test_unknown_adapter():
    with pytest.raises(ValueError):get_adapter("missing")
