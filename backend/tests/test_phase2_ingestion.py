from app.ingestion.extractor import extract_claims
from app.ingestion.canonicalizer import normalize_name
from app.ingestion.parser import parse_html

def test_normalization():
    assert normalize_name("University of   Test!")=="university of test"

def test_jsonld_extraction():
    claims=extract_claims("Admissions","", [{"@type":"College","name":"Example University","url":"https://example.edu"}])
    assert any(c.entity_type=="institution" and c.field=="canonical_name" for c in claims)

def test_html_parser():
    title,text,structured=parse_html("<html><head><title>Hello</title></head><body><h1>Admissions</h1></body></html>")
    assert title=="Hello"
    assert "Admissions" in text
