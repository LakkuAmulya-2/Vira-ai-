"""phase 3 source intelligence
Revision ID: 0004_phase3_source_intelligence
Revises: 0003_phase2_ingestion_indexes
"""
from alembic import op
import sqlalchemy as sa
revision="0004_phase3_source_intelligence"
down_revision="0003_phase2_ingestion_indexes"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("source_profiles",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("name",sa.String(200),nullable=False),sa.Column("base_url",sa.String(2048),nullable=False),sa.Column("region",sa.String(32),nullable=False),sa.Column("country_code",sa.String(2)),sa.Column("category",sa.String(64),nullable=False),sa.Column("entity_type",sa.String(64),nullable=False),sa.Column("adapter_key",sa.String(64),nullable=False),sa.Column("allowed_paths",sa.JSON(),nullable=False),sa.Column("crawl_interval_seconds",sa.Integer(),nullable=False),sa.Column("enabled",sa.Boolean(),nullable=False),sa.UniqueConstraint("name"),sa.UniqueConstraint("base_url"))
    op.create_table("source_runs",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("source_profile_id",sa.String(),sa.ForeignKey("source_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("job_id",sa.String(64),nullable=False),sa.Column("url",sa.String(2048),nullable=False),sa.Column("status",sa.String(32),nullable=False),sa.Column("adapter_key",sa.String(64),nullable=False),sa.Column("result",sa.JSON()),sa.Column("error",sa.String(4000)),sa.UniqueConstraint("job_id"))
    op.create_index("ix_source_profiles_region_country","source_profiles",["region","country_code"])
    op.create_index("ix_source_runs_profile_status","source_runs",["source_profile_id","status"])
def downgrade():
    op.drop_index("ix_source_runs_profile_status",table_name="source_runs");op.drop_index("ix_source_profiles_region_country",table_name="source_profiles");op.drop_table("source_runs");op.drop_table("source_profiles")
