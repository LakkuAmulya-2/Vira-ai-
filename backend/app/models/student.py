from datetime import date
from sqlalchemy import BigInteger, Date, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDTimestampMixin


class StudentProfile(UUIDTimestampMixin, Base):
    __tablename__ = "student_profiles"

    user_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(32), nullable=True)
    country_code: Mapped[str] = mapped_column(String(2))
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    education_stage: Mapped[str] = mapped_column(String(32))
    preferred_countries: Mapped[list[str]] = mapped_column(JSON, default=list)
    preferred_languages: Mapped[list[str]] = mapped_column(JSON, default=list)
    budget_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    annual_budget_minor: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    interests: Mapped[list["StudentInterest"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )
    skills: Mapped[list["StudentSkill"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )
    goals: Mapped[list["CareerGoal"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class StudentInterest(UUIDTimestampMixin, Base):
    __tablename__ = "student_interests"
    __table_args__ = (UniqueConstraint("student_id", "name"),)

    student_id: Mapped[str] = mapped_column(ForeignKey("student_profiles.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))
    weight: Mapped[int] = mapped_column(Integer, default=1)
    student: Mapped[StudentProfile] = relationship(back_populates="interests")


class StudentSkill(UUIDTimestampMixin, Base):
    __tablename__ = "student_skills"
    __table_args__ = (UniqueConstraint("student_id", "name"),)

    student_id: Mapped[str] = mapped_column(ForeignKey("student_profiles.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))
    proficiency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    student: Mapped[StudentProfile] = relationship(back_populates="skills")


class CareerGoal(UUIDTimestampMixin, Base):
    __tablename__ = "career_goals"
    __table_args__ = (UniqueConstraint("student_id", "title"),)

    student_id: Mapped[str] = mapped_column(ForeignKey("student_profiles.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(160))
    priority: Mapped[int] = mapped_column(Integer, default=1)
    student: Mapped[StudentProfile] = relationship(back_populates="goals")
