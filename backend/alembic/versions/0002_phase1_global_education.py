"""phase 1 global education canonical data
Revision ID: 0002_phase1_global_education
Revises:
Create Date: 2026-09-01
"""
from alembic import op
import sqlalchemy as sa
revision="0002_phase1_global_education"
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    op.create_table("countries",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("iso_code",sa.String(2),nullable=False),sa.Column("name",sa.String(120),nullable=False),sa.Column("region",sa.String(80),nullable=False),sa.UniqueConstraint("iso_code"),sa.UniqueConstraint("name"))
    for name,cols in {
      "institutions":[sa.Column("canonical_name",sa.String(300),nullable=False),sa.Column("country_code",sa.String(2),sa.ForeignKey("countries.iso_code"),nullable=False),sa.Column("official_url",sa.String(2048)),sa.Column("institution_type",sa.String(80),nullable=False),sa.Column("status",sa.String(32),nullable=False)],
      "courses":[sa.Column("canonical_name",sa.String(300),nullable=False),sa.Column("field_of_study",sa.String(160),nullable=False),sa.Column("level",sa.String(80),nullable=False),sa.Column("status",sa.String(32),nullable=False)],
      "programs":[sa.Column("institution_id",sa.String(),sa.ForeignKey("institutions.id",ondelete="CASCADE"),nullable=False),sa.Column("course_id",sa.String(),sa.ForeignKey("courses.id"),nullable=False),sa.Column("official_name",sa.String(400),nullable=False),sa.Column("duration_months",sa.Integer()),sa.Column("delivery_mode",sa.String(64)),sa.Column("tuition",sa.JSON()),sa.Column("eligibility",sa.JSON()),sa.Column("official_url",sa.String(2048)),sa.Column("status",sa.String(32),nullable=False)],
      "scholarships":[sa.Column("canonical_name",sa.String(400),nullable=False),sa.Column("provider_name",sa.String(300),nullable=False),sa.Column("country_code",sa.String(2),sa.ForeignKey("countries.iso_code")),sa.Column("amount",sa.JSON()),sa.Column("eligibility",sa.JSON()),sa.Column("application_url",sa.String(2048)),sa.Column("deadline",sa.Date()),sa.Column("status",sa.String(32),nullable=False)],
      "entrance_exams":[sa.Column("canonical_name",sa.String(240),nullable=False),sa.Column("country_code",sa.String(2),sa.ForeignKey("countries.iso_code")),sa.Column("organizer",sa.String(300)),sa.Column("official_url",sa.String(2048)),sa.Column("requirements",sa.JSON()),sa.Column("status",sa.String(32),nullable=False)],
      "education_facts":[sa.Column("entity_type",sa.String(64),nullable=False),sa.Column("entity_id",sa.String(64),nullable=False),sa.Column("field",sa.String(160),nullable=False),sa.Column("value",sa.JSON(),nullable=False),sa.Column("source_id",sa.String(),sa.ForeignKey("data_sources.id"),nullable=False),sa.Column("document_id",sa.String(),sa.ForeignKey("source_documents.id",ondelete="SET NULL")),sa.Column("effective_from",sa.DateTime(timezone=True)),sa.Column("effective_until",sa.DateTime(timezone=True)),sa.Column("confidence",sa.Numeric(4,3)),sa.Column("status",sa.String(32),nullable=False)]
    }.items():
      op.create_table(name,sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),*cols)

def downgrade():
    for n in ["education_facts","entrance_exams","scholarships","programs","courses","institutions","countries"]: op.drop_table(n)
