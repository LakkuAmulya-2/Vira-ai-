from sqlalchemy import JSON,String,Text,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base,UUIDTimestampMixin

class AgentExecution(UUIDTimestampMixin,Base):
    __tablename__="agent_executions"
    user_id:Mapped[str]=mapped_column(String(64),index=True)
    conversation_id:Mapped[str|None]=mapped_column(String(64),nullable=True,index=True)
    status:Mapped[str]=mapped_column(String(32),index=True)
    primary_agent:Mapped[str]=mapped_column(String(64),index=True)
    plan:Mapped[dict]=mapped_column(JSON)
    final_result:Mapped[dict|None]=mapped_column(JSON,nullable=True)

class AgentTaskExecution(UUIDTimestampMixin,Base):
    __tablename__="agent_task_executions"
    execution_id:Mapped[str]=mapped_column(ForeignKey("agent_executions.id",ondelete="CASCADE"),index=True)
    task_id:Mapped[str]=mapped_column(String(64),index=True)
    agent:Mapped[str]=mapped_column(String(64),index=True)
    status:Mapped[str]=mapped_column(String(32),index=True)
    input:Mapped[dict]=mapped_column(JSON)
    output:Mapped[dict|None]=mapped_column(JSON,nullable=True)
    error:Mapped[str|None]=mapped_column(Text,nullable=True)
    latency_ms:Mapped[int]=mapped_column(default=0)
