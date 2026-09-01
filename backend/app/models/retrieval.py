from typing import Any
from sqlalchemy import ForeignKey,JSON,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base,UUIDTimestampMixin

class KnowledgeEmbedding(UUIDTimestampMixin,Base):
    __tablename__="knowledge_embeddings"
    claim_id:Mapped[str]=mapped_column(ForeignKey("knowledge_claims.id",ondelete="CASCADE"),unique=True,index=True)
    model:Mapped[str]=mapped_column(String(160),index=True)
    dimensions:Mapped[int]=mapped_column()
    embedding:Mapped[list[float]]=mapped_column(JSON)
    content:Mapped[str]=mapped_column(Text)
    content_hash:Mapped[str]=mapped_column(String(64),index=True)
    status:Mapped[str]=mapped_column(String(32),default="READY",index=True)

class RetrievalAudit(UUIDTimestampMixin,Base):
    __tablename__="retrieval_audits"
    query_hash:Mapped[str]=mapped_column(String(64),index=True)
    user_id:Mapped[str|None]=mapped_column(String(64),nullable=True,index=True)
    filters:Mapped[dict[str,Any]|None]=mapped_column(JSON,nullable=True)
    result_count:Mapped[int]=mapped_column()
