from sqlalchemy import ForeignKey,Integer,JSON,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import Base,UUIDTimestampMixin

class StudentAcademicRecord(UUIDTimestampMixin,Base):
    __tablename__="student_academic_records"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    qualification:Mapped[str]=mapped_column(String(120))
    board_or_system:Mapped[str|None]=mapped_column(String(120),nullable=True)
    score:Mapped[float|None]=mapped_column(nullable=True)
    score_scale:Mapped[float|None]=mapped_column(nullable=True)
    graduation_year:Mapped[int|None]=mapped_column(Integer,nullable=True)

class StudentConstraint(UUIDTimestampMixin,Base):
    __tablename__="student_constraints"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    category:Mapped[str]=mapped_column(String(80))
    value:Mapped[str]=mapped_column(Text)
    importance:Mapped[int]=mapped_column(Integer,default=3)

class StudentIntelligenceSnapshot(UUIDTimestampMixin,Base):
    __tablename__="student_intelligence_snapshots"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    profile_version:Mapped[str]=mapped_column(String(32))
    completeness_score:Mapped[float]=mapped_column()
    profile:Mapped[dict]=mapped_column(JSON)
    assumptions:Mapped[list]=mapped_column(JSON,default=list)
    active:Mapped[bool]=mapped_column(default=True,index=True)

class StudentMemory(UUIDTimestampMixin,Base):
    __tablename__="student_memories"
    student_id:Mapped[str]=mapped_column(ForeignKey("student_profiles.id",ondelete="CASCADE"),index=True)
    namespace:Mapped[str]=mapped_column(String(80),index=True)
    memory_key:Mapped[str]=mapped_column(String(160))
    value:Mapped[dict]=mapped_column(JSON)
    confidence:Mapped[float]=mapped_column(default=1.0)
    source:Mapped[str]=mapped_column(String(64))
    expires_at:Mapped[str|None]=mapped_column(String(64),nullable=True)
    __table_args__=(UniqueConstraint("student_id","namespace","memory_key"),)
