from abc import ABC,abstractmethod
from dataclasses import dataclass
from app.ingestion.extractor import ExtractedClaim
from app.ingestion.parser import parse_document

@dataclass(frozen=True)
class AdapterContext:
    region:str
    country_code:str|None
    category:str
    entity_type:str

class SourceAdapter(ABC):
    key:str

    @abstractmethod
    def extract(self,content:str,content_type:str|None,context:AdapterContext)->tuple[str|None,list[ExtractedClaim]]:
        raise NotImplementedError

class GenericEducationAdapter(SourceAdapter):
    key="generic"
    def extract(self,content,content_type,context):
        from app.ingestion.extractor import extract_claims
        title,text,structured=parse_document(content,content_type)
        return title,extract_claims(title,text,structured,context.entity_type)
