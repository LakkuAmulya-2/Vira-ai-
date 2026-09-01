import hashlib
from app.retrieval.contracts import Citation

def citation_for(claim,source,document=None)->Citation:
    raw=f"{claim.id}:{source.id}:{getattr(document,'id','')}"
    return Citation(citation_id=hashlib.sha256(raw.encode()).hexdigest()[:16],claim_id=claim.id,entity_type=claim.entity_type,entity_key=claim.entity_key,field=claim.field,source_name=source.name,source_url=source.base_url,document_url=getattr(document,"url",None),country_code=claim.country_code,jurisdiction=claim.jurisdiction)
