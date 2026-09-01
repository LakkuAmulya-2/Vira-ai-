from collections.abc import Sequence
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(pattern="^(system|user|assistant|tool)$")
    content: str


class StructuredGeneration(BaseModel):
    content: str
    metadata: dict = Field(default_factory=dict)


class AIProvider:
    async def generate(
        self,
        messages: Sequence[Message],
        *,
        temperature: float = 0.2,
    ) -> StructuredGeneration:
        raise NotImplementedError
