from app.source_intelligence.adapters.base import GenericEducationAdapter,SourceAdapter
from app.source_intelligence.adapters.india import IndiaOfficialAdapter
from app.source_intelligence.adapters.us import USOfficialAdapter
from app.source_intelligence.adapters.uk import UKOfficialAdapter
from app.source_intelligence.adapters.eu import EUOfficialAdapter
from app.source_intelligence.adapters.gulf import GulfOfficialAdapter

_ADAPTERS={x.key:x for x in [GenericEducationAdapter,IndiaOfficialAdapter,USOfficialAdapter,UKOfficialAdapter,EUOfficialAdapter,GulfOfficialAdapter]}

def get_adapter(key:str)->SourceAdapter:
    cls=_ADAPTERS.get(key)
    if cls is None: raise ValueError(f"Unknown adapter_key: {key}")
    return cls()
