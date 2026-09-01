import logging,json
from datetime import datetime,timezone
logger=logging.getLogger("vira.audit")
def audit(event_type:str,actor_id:str|None=None,resource_type:str|None=None,resource_id:str|None=None,metadata:dict|None=None)->None:
    logger.info(json.dumps({"event_type":event_type,"actor_id":actor_id,"resource_type":resource_type,"resource_id":resource_id,"metadata":metadata or {},"timestamp":datetime.now(timezone.utc).isoformat()},default=str))
