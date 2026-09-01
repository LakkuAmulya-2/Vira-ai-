from datetime import date,datetime
from sqlalchemy import Date,DateTime,ForeignKey,JSON,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base,UUIDTimestampMixin

class Application(UUIDTimestampMixin,Base):
    __tablename__="applications"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    entity_type:Mapped[str]=mapped_column(String(64),index=True)
    entity_key:Mapped[str]=mapped_column(String(240),index=True)
    title:Mapped[str]=mapped_column(String(400))
    status:Mapped[str]=mapped_column(String(40),default="PLANNING",index=True)
    application_url:Mapped[str|None]=mapped_column(String(2048),nullable=True)
    deadline:Mapped[date|None]=mapped_column(Date,nullable=True,index=True)
    metadata_json:Mapped[dict]=mapped_column(JSON,default=dict)
    __table_args__=(UniqueConstraint("student_id","entity_type","entity_key"),)

class ApplicationTask(UUIDTimestampMixin,Base):
    __tablename__="application_tasks"
    application_id:Mapped[str]=mapped_column(ForeignKey("applications.id",ondelete="CASCADE"),index=True)
    task_type:Mapped[str]=mapped_column(String(80))
    title:Mapped[str]=mapped_column(String(400))
    status:Mapped[str]=mapped_column(String(40),default="TODO",index=True)
    due_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True,index=True)
    payload:Mapped[dict]=mapped_column(JSON,default=dict)

class ApplicationDocument(UUIDTimestampMixin,Base):
    __tablename__="application_documents"
    application_id:Mapped[str]=mapped_column(ForeignKey("applications.id",ondelete="CASCADE"),index=True)
    document_type:Mapped[str]=mapped_column(String(120))
    status:Mapped[str]=mapped_column(String(40),default="MISSING")
    storage_key:Mapped[str|None]=mapped_column(String(1024),nullable=True)
    verification:Mapped[dict]=mapped_column(JSON,default=dict)
    __table_args__=(UniqueConstraint("application_id","document_type"),)

class ApplicationEvent(UUIDTimestampMixin,Base):
    __tablename__="application_events"
    application_id:Mapped[str]=mapped_column(ForeignKey("applications.id",ondelete="CASCADE"),index=True)
    event_type:Mapped[str]=mapped_column(String(100),index=True)
    message:Mapped[str]=mapped_column(Text)
    payload:Mapped[dict]=mapped_column(JSON,default=dict)
