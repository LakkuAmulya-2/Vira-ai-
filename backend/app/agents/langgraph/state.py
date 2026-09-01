from typing import Annotated,TypedDict
from langgraph.graph.message import add_messages
class ViraAgentState(TypedDict,total=False):
    messages:Annotated[list,add_messages]
    request:dict
    user_id:str
    conversation_id:str|None
    plan:dict
    tasks:list[dict]
    task_index:int
    results:list[dict]
    final:dict
    error:str|None
