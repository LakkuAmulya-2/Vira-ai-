import json,re
from html import unescape
from bs4 import BeautifulSoup

def parse_html(content:str)->tuple[str|None,str,list[dict]]:
    soup=BeautifulSoup(content,"html.parser")
    for tag in soup(["script","style","noscript"]):
        if tag.name!="script" or tag.get("type")!="application/ld+json": tag.decompose()
    title=soup.title.get_text(" ",strip=True) if soup.title else None
    text=" ".join(unescape(soup.get_text(" ",strip=True)).split())
    structured=[]
    raw_soup=BeautifulSoup(content,"html.parser")
    for script in raw_soup.find_all("script",attrs={"type":"application/ld+json"}):
        try:
            data=json.loads(script.string or script.get_text())
            structured.extend(data if isinstance(data,list) else [data])
        except (json.JSONDecodeError,TypeError): pass
    return title,text,structured

def parse_document(content:str,content_type:str|None)->tuple[str|None,str,list[dict]]:
    if content_type and "html" in content_type.lower(): return parse_html(content)
    return None," ".join(content.split()),[]
