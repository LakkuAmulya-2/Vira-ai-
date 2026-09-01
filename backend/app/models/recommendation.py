from typing import Any
from sqlalchemy import ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDTimestampMixin


class RecommendationRun(UUIDTimestampMixin, Base):
    __tablename__ = "recommendation_runs"

    student_id: Mapped[str] = mapped_column(ForeignKey("student_profiles.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(32), default="GENERATED")
    algorithm_version: Mapped[str] = mapped_column(String(64))
    input_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON)


class RecommendationItem(UUIDTimestampMixin, Base):
    __tablename__ = "recommendation_items"

    run_id: Mapped[str] = mapped_column(ForeignKey("recommendation_runs.id", ondelete="CASCADE"))
    entity_type: Mapped[str] = mapped_column(String(64))
    entity_key: Mapped[str] = mapped_column(String(240))
    score: Mapped[float] = mapped_column(Numeric(5, 4))
    reasons: Mapped[list[str]] = mapped_column(JSON)
    evidence: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
