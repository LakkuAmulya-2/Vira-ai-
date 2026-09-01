from enum import StrEnum
from pydantic import BaseModel,Field
from app.agents.contracts import AgentName,AgentResult

class ExecutionStatus(StrEnum):
    PLANNED="PLANNED";RUNNING="RUNNING";COMPLETED="COMPLETED";FAILED="FAILED";BLOCKED="BLOCKED"

class ToolCall(BaseModel):
    tool:str
    arguments:dict=Field(default_factory=dict)

class AgentTask(BaseModel):
    task_id:str
    agent:AgentName
    objective:str
    tool_calls:list[ToolCall]=Field(default_factory=list)
    depends_on:list[str]=Field(default_factory=list)

class ExecutionPlan(BaseModel):
    primary_agent:AgentName
    tasks:list[AgentTask]
    reason:str
    max_steps:int

class TaskResult(BaseModel):
    task_id:str
    agent:AgentName
    status:ExecutionStatus
    result:AgentResult|None=None
    error:str|None=None
    latency_ms:int=0

class OrchestrationResponse(BaseModel):
    plan:ExecutionPlan
    results:list[TaskResult]
    final:AgentResult
    confidence:float=Field(ge=0,le=1)
