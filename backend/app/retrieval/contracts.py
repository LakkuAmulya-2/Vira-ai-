from pydantic import BaseModel,Field

class RetrievalRequest(BaseModel):
    query:str=Field(min_length=2,max_length=2000)
    entity_type:str|None=None
    country_code:str|None=Field(default=None,min_length=2,max_length=2)
    jurisdiction:str|None=None
    limit:int=Field(default=12,ge=1,le=50)
    lexical_weight:float=Field(default=0.45,ge=0,max=1)
    vector_weight:float=Field(default=0.55,ge=0,max=1)

class Citation(BaseModel):
    citation_id:str
    claim_id:str|None=None
    entity_type:str
    entity_key:str
    field:str
    source_name:str
    source_url:str
    document_url:str|None=None
    country_code:str|None=None
    jurisdiction:str|None=None

class RetrievalHit(BaseModel):
    citation:Citation
    value:object
    score:float
    lexical_score:float=0
    vector_score:float=0
    excerpt:str

class RetrievalResponse(BaseModel):
    query:str
    hits:list[RetrievalHit]
    context:str
    total:int

class GroundedContextRequest(RetrievalRequest):
    max_context_chars:int=Field(default=12000,ge=500,max=50000)
