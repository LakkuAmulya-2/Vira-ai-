from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,JSON,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base,UUIDTimestampMixin

class StudentAlert(UUIDTimestampMixin,Base):
    __tablename__="student_alerts"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    alert_type:Mapped[str]=mapped_column(String(80),index=True)
    entity_type:Mapped[str|None]=mapped_column(String(80),nullable=True)
    entity_key:Mapped[str|None]=mapped_column(String(240),nullable=True)
    priority:Mapped[str]=mapped_column(String(24),default="NORMAL",index=True)
    status:Mapped[str]=mapped_column(String(32),default="PENDING",index=True)
    title:Mapped[str]=mapped_column(String(400))
    body:Mapped[str]=mapped_column(Text)
    action_url:Mapped[str|None]=mapped_column(String(2048),nullable=True)
    payload:Mapped[dict]=mapped_column(JSON,default=dict)
    dedupe_key:Mapped[str]=mapped_column(String(240),unique=True,index=True)

class NotificationPreference(UUIDTimestampMixin,Base):
    __tablename__="notification_preferences"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),unique=True,index=True)
    deadline_alerts:Mapped[bool]=mapped_column(default=True)
    scholarship_alerts:Mapped[bool]=mapped_column(default=True)
    admission_alerts:Mapped[bool]=mapped_column(default=True)
    exam_alerts:Mapped[bool]=mapped_column(default=True)
    channels:Mapped[dict]=mapped_column(JSON,default=lambda:{"in_app":True})
    quiet_hours:Mapped[dict]=mapped_column(JSON,default=dict)
