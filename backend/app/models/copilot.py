from sqlalchemy import ForeignKey,JSON,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base,UUIDTimestampMixin

class CopilotConversation(UUIDTimestampMixin,Base):
    __tablename__="copilot_conversations"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    title:Mapped[str]=mapped_column(String(400),default="Vira conversation")
    status:Mapped[str]=mapped_column(String(32),default="ACTIVE",index=True)
    context_snapshot:Mapped[dict]=mapped_column(JSON,default=dict)

class CopilotMessage(UUIDTimestampMixin,Base):
    __tablename__="copilot_messages"
    conversation_id:Mapped[str]=mapped_column(ForeignKey("copilot_conversations.id",ondelete="CASCADE"),index=True)
    role:Mapped[str]=mapped_column(String(24),index=True)
    content:Mapped[str]=mapped_column(Text)
    metadata_json:Mapped[dict]=mapped_column(JSON,default=dict)

class CopilotAction(UUIDTimestampMixin,Base):
    __tablename__="copilot_actions"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    conversation_id:Mapped[str|None]=mapped_column(ForeignKey("copilot_conversations.id",ondelete="SET NULL"),nullable=True,index=True)
    action_type:Mapped[str]=mapped_column(String(100),index=True)
    title:Mapped[str]=mapped_column(String(400))
    status:Mapped[str]=mapped_column(String(32),default="PROPOSED",index=True)
    requires_confirmation:Mapped[bool]=mapped_column(default=True)
    payload:Mapped[dict]=mapped_column(JSON,default=dict)
    result:Mapped[dict|None]=mapped_column(JSON,nullable=True)
