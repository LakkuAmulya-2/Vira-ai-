import hashlib,math,re
from collections import Counter

def build_claim_content(entity_type:str,entity_key:str,field:str,value:object)->str:
    return f"{entity_type} | {entity_key} | {field} | {value}"

def deterministic_embedding(text:str,dimensions:int=256)->list[float]:
    vector=[0.0]*dimensions
    for token in re.findall(r"[a-z0-9_]{2,}",text.lower()):
        digest=hashlib.sha256(token.encode()).digest()
        for offset in range(0,8,2):
            idx=int.from_bytes(digest[offset:offset+2],"big")%dimensions
            vector[idx]+=1.0 if digest[offset]%2 else -1.0
    norm=math.sqrt(sum(v*v for v in vector))
    return [v/norm for v in vector] if norm else vector

def cosine_similarity(a:list[float],b:list[float])->float:
    if not a or not b:return 0.0
    dot=sum(x*y for x,y in zip(a,b));na=math.sqrt(sum(x*x for x in a));nb=math.sqrt(sum(y*y for y in b))
    return dot/(na*nb) if na and nb else 0.0

def content_hash(text:str)->str:return hashlib.sha256(text.encode()).hexdigest()
