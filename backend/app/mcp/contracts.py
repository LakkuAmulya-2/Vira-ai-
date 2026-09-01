from pydantic import BaseModel, Field


class MCPToolRequest(BaseModel):
    server: str = Field(min_length=1, max_length=120)
    tool: str = Field(min_length=1, max_length=120)
    arguments: dict = Field(default_factory=dict)


class MCPToolResponse(BaseModel):
    content: dict
    source: str
