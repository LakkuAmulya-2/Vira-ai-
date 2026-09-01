from pydantic import BaseModel,Field
class EvaluationCase(BaseModel):
    name:str
    query:str
    expected_capabilities:list[str]=Field(default_factory=list)
class EvaluationResult(BaseModel):
    name:str
    passed:bool
    score:float
    details:dict=Field(default_factory=dict)
