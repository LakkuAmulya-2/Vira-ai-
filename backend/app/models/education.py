from datetime import date, datetime
from typing import Any
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, JSON, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDTimestampMixin

class Country(UUIDTimestampMixin, Base):
    __tablename__="countries"
    iso_code: Mapped[str]=mapped_column(String(2), unique=True, index=True)
    name: Mapped[str]=mapped_column(String(120), unique=True)
    region: Mapped[str]=mapped_column(String(80))

class Institution(UUIDTimestampMixin, Base):
    __tablename__="institutions"
    canonical_name: Mapped[str]=mapped_column(String(300), index=True)
    country_code: Mapped[str]=mapped_column(ForeignKey("countries.iso_code"), index=True)
    official_url: Mapped[str|None]=mapped_column(String(2048), nullable=True)
    institution_type: Mapped[str]=mapped_column(String(80), index=True)
    status: Mapped[str]=mapped_column(String(32), default="PENDING_VERIFICATION", index=True)
    __table_args__=(UniqueConstraint("canonical_name","country_code",name="uq_institution_country_name"),)

class Course(UUIDTimestampMixin, Base):
    __tablename__="courses"
    canonical_name: Mapped[str]=mapped_column(String(300), index=True)
    field_of_study: Mapped[str]=mapped_column(String(160), index=True)
    level: Mapped[str]=mapped_column(String(80), index=True)
    status: Mapped[str]=mapped_column(String(32), default="PENDING_VERIFICATION", index=True)
    __table_args__=(UniqueConstraint("canonical_name","field_of_study","level",name="uq_course_canonical"),)

class Program(UUIDTimestampMixin, Base):
    __tablename__="programs"
    institution_id: Mapped[str]=mapped_column(ForeignKey("institutions.id",ondelete="CASCADE"), index=True)
    course_id: Mapped[str]=mapped_column(ForeignKey("courses.id",ondelete="RESTRICT"), index=True)
    official_name: Mapped[str]=mapped_column(String(400))
    duration_months: Mapped[int|None]=mapped_column(nullable=True)
    delivery_mode: Mapped[str|None]=mapped_column(String(64),nullable=True)
    tuition: Mapped[dict|None]=mapped_column(JSON,nullable=True)
    eligibility: Mapped[dict|None]=mapped_column(JSON,nullable=True)
    official_url: Mapped[str|None]=mapped_column(String(2048),nullable=True)
    status: Mapped[str]=mapped_column(String(32),default="PENDING_VERIFICATION",index=True)
    __table_args__=(UniqueConstraint("institution_id","official_name",name="uq_program_institution_name"),)

class Scholarship(UUIDTimestampMixin, Base):
    __tablename__="scholarships"
    canonical_name: Mapped[str]=mapped_column(String(400), index=True)
    provider_name: Mapped[str]=mapped_column(String(300))
    country_code: Mapped[str|None]=mapped_column(ForeignKey("countries.iso_code"),nullable=True,index=True)
    amount: Mapped[dict|None]=mapped_column(JSON,nullable=True)
    eligibility: Mapped[dict|None]=mapped_column(JSON,nullable=True)
    application_url: Mapped[str|None]=mapped_column(String(2048),nullable=True)
    deadline: Mapped[date|None]=mapped_column(Date,nullable=True,index=True)
    status: Mapped[str]=mapped_column(String(32),default="PENDING_VERIFICATION",index=True)

class EntranceExam(UUIDTimestampMixin, Base):
    __tablename__="entrance_exams"
    canonical_name: Mapped[str]=mapped_column(String(240), index=True)
    country_code: Mapped[str|None]=mapped_column(ForeignKey("countries.iso_code"),nullable=True,index=True)
    organizer: Mapped[str|None]=mapped_column(String(300),nullable=True)
    official_url: Mapped[str|None]=mapped_column(String(2048),nullable=True)
    requirements: Mapped[dict|None]=mapped_column(JSON,nullable=True)
    status: Mapped[str]=mapped_column(String(32),default="PENDING_VERIFICATION",index=True)
    __table_args__=(UniqueConstraint("canonical_name","country_code",name="uq_exam_country_name"),)

class EducationFact(UUIDTimestampMixin, Base):
    __tablename__="education_facts"
    entity_type: Mapped[str]=mapped_column(String(64),index=True)
    entity_id: Mapped[str]=mapped_column(String(64),index=True)
    field: Mapped[str]=mapped_column(String(160),index=True)
    value: Mapped[Any]=mapped_column(JSON)
    source_id: Mapped[str]=mapped_column(ForeignKey("data_sources.id",ondelete="RESTRICT"),index=True)
    document_id: Mapped[str|None]=mapped_column(ForeignKey("source_documents.id",ondelete="SET NULL"),nullable=True)
    effective_from: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    effective_until: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    confidence: Mapped[float|None]=mapped_column(Numeric(4,3),nullable=True)
    status: Mapped[str]=mapped_column(String(32),default="PENDING",index=True)
    __table_args__=(UniqueConstraint("entity_type","entity_id","field","source_id",name="uq_fact_provenance"),)
