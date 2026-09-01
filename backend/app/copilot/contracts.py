from pydantic import BaseModel,Field
class CopilotRequest(BaseModel):
    message:str=Field(min_length=1,max_length=12000)
    conversation_id:str|None=None
class ActionDecision(BaseModel):
    approved:bool
class CopilotResponse(BaseModel):
    conversation_id:str
    message:str
    agent_result:dict
    proposed_actions:list[dict]=Field(default_factory=list)
