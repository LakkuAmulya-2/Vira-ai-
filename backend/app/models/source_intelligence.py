from sqlalchemy import Boolean,Integer,JSON,String,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base,UUIDTimestampMixin

class SourceProfile(UUIDTimestampMixin,Base):
    __tablename__="source_profiles"
    name:Mapped[str]=mapped_column(String(200),unique=True)
    base_url:Mapped[str]=mapped_column(String(2048),unique=True)
    region:Mapped[str]=mapped_column(String(32),index=True)
    country_code:Mapped[str|None]=mapped_column(String(2),nullable=True,index=True)
    category:Mapped[str]=mapped_column(String(64),index=True)
    entity_type:Mapped[str]=mapped_column(String(64),index=True)
    adapter_key:Mapped[str]=mapped_column(String(64),index=True)
    allowed_paths:Mapped[list]=mapped_column(JSON,default=list)
    crawl_interval_seconds:Mapped[int]=mapped_column(Integer,default=86400)
    enabled:Mapped[bool]=mapped_column(Boolean,default=True,index=True)

class SourceRun(UUIDTimestampMixin,Base):
    __tablename__="source_runs"
    source_profile_id:Mapped[str]=mapped_column(ForeignKey("source_profiles.id",ondelete="CASCADE"),index=True)
    job_id:Mapped[str]=mapped_column(String(64),unique=True,index=True)
    url:Mapped[str]=mapped_column(String(2048))
    status:Mapped[str]=mapped_column(String(32),default="QUEUED",index=True)
    adapter_key:Mapped[str]=mapped_column(String(64))
    result:Mapped[dict|None]=mapped_column(JSON,nullable=True)
    error:Mapped[str|None]=mapped_column(String(4000),nullable=True)
