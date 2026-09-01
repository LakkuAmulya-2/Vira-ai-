import hashlib
from uuid import uuid4
import httpx

async def fetch_content(url:str)->tuple[str,str]:
    async with httpx.AsyncClient(timeout=20,follow_redirects=True) as client:
        response=await client.get(url,headers={"User-Agent":"ViraKnowledgeBot/1.0"})
        response.raise_for_status()
        body=response.text
    return body,hashlib.sha256(body.encode("utf-8")).hexdigest()

async def fetch_content_with_metadata(url:str)->tuple[str,str,str|None]:
    async with httpx.AsyncClient(timeout=20,follow_redirects=True) as client:
        response=await client.get(url,headers={"User-Agent":"ViraKnowledgeBot/1.0"})
        response.raise_for_status()
        body=response.text
        return body,hashlib.sha256(body.encode("utf-8")).hexdigest(),response.headers.get("content-type")

def create_job_id()->str:return str(uuid4())
