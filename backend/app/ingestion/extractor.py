import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ExtractedClaim:
    entity_type:str
    entity_key:str
    field:str
    value:object
    confidence:float

_TYPE_MAP={"college":"institution","university":"institution","educationalorganization":"institution","course":"course","scholarship":"scholarship","event":"entrance_exam"}

def _claim(entity_type,key,field,value,confidence=0.6):
    return ExtractedClaim(entity_type,key,field,value,confidence)

def extract_claims(title:str|None,text:str,structured:list[dict],fallback_entity_type:str|None=None)->list[ExtractedClaim]:
    claims=[]
    for node in structured:
        if not isinstance(node,dict): continue
        raw=node.get("@type","")
        types=raw if isinstance(raw,list) else [raw]
        entity_type=next((_TYPE_MAP.get(str(t).lower()) for t in types if _TYPE_MAP.get(str(t).lower())),fallback_entity_type)
        name=node.get("name")
        if entity_type and name:
            claims.append(_claim(entity_type,str(name).strip(),"canonical_name",str(name).strip(),0.95))
            for field in ("url","description","provider","organizer","startDate","endDate"):
                if node.get(field): claims.append(_claim(entity_type,str(name).strip(),field,node[field],0.8))
    if fallback_entity_type and title:
        claims.append(_claim(fallback_entity_type,title[:240],"title",title,0.45))
    for label,field in [("deadline","deadline"),("tuition","tuition"),("eligibility","eligibility"),("duration","duration")]:
        match=re.search(rf"(.{{0,80}}{label}.{{0,160}})",text,re.I)
        if match and fallback_entity_type:
            key=(title or fallback_entity_type)[:240]
            claims.append(_claim(fallback_entity_type,key,field,match.group(1).strip(),0.35))
    dedup={}
    for c in claims: dedup[(c.entity_type,c.entity_key,c.field,str(c.value))]=c
    return list(dedup.values())
