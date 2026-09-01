from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDTimestampMixin


class DataSource(UUIDTimestampMixin, Base):
    __tablename__ = "data_sources"

    name: Mapped[str] = mapped_column(String(200))
    base_url: Mapped[str] = mapped_column(String(2048), unique=True)
    source_type: Mapped[str] = mapped_column(String(64))
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    jurisdiction: Mapped[str | None] = mapped_column(String(160), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(32), default="PENDING")
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SourceDocument(UUIDTimestampMixin, Base):
    __tablename__ = "source_documents"

    source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(2048), unique=True)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(256), nullable=True)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="PENDING")


class KnowledgeClaim(UUIDTimestampMixin, Base):
    __tablename__ = "knowledge_claims"

    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_key: Mapped[str] = mapped_column(String(240), index=True)
    field: Mapped[str] = mapped_column(String(160))
    value: Mapped[Any] = mapped_column(JSON)
    source_id: Mapped[str] = mapped_column(ForeignKey("data_sources.id", ondelete="RESTRICT"))
    document_id: Mapped[str | None] = mapped_column(
        ForeignKey("source_documents.id", ondelete="SET NULL"), nullable=True
    )
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True)
    jurisdiction: Mapped[str | None] = mapped_column(String(160), nullable=True)
    effective_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
