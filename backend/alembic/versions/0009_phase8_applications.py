"""phase 8 application journey
Revision ID: 0009_phase8_applications
Revises: 0008_phase7_recommendation_decisions
"""
from alembic import op
import sqlalchemy as sa
revision="0009_phase8_applications";down_revision="0008_phase7_recommendation_decisions";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("applications",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("entity_type",sa.String(64),nullable=False),sa.Column("entity_key",sa.String(240),nullable=False),sa.Column("title",sa.String(400),nullable=False),sa.Column("status",sa.String(40),nullable=False),sa.Column("application_url",sa.String(2048)),sa.Column("deadline",sa.Date()),sa.Column("metadata_json",sa.JSON(),nullable=False),sa.UniqueConstraint("student_id","entity_type","entity_key"))
 op.create_table("application_tasks",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("application_id",sa.String(),sa.ForeignKey("applications.id",ondelete="CASCADE"),nullable=False),sa.Column("task_type",sa.String(80),nullable=False),sa.Column("title",sa.String(400),nullable=False),sa.Column("status",sa.String(40),nullable=False),sa.Column("due_at",sa.DateTime(timezone=True)),sa.Column("payload",sa.JSON(),nullable=False))
 op.create_table("application_documents",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("application_id",sa.String(),sa.ForeignKey("applications.id",ondelete="CASCADE"),nullable=False),sa.Column("document_type",sa.String(120),nullable=False),sa.Column("status",sa.String(40),nullable=False),sa.Column("storage_key",sa.String(1024)),sa.Column("verification",sa.JSON(),nullable=False),sa.UniqueConstraint("application_id","document_type"))
 op.create_table("application_events",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("application_id",sa.String(),sa.ForeignKey("applications.id",ondelete="CASCADE"),nullable=False),sa.Column("event_type",sa.String(100),nullable=False),sa.Column("message",sa.Text(),nullable=False),sa.Column("payload",sa.JSON(),nullable=False))
 for table,cols in [("applications",["student_id","status","deadline"]),("application_tasks",["application_id","status","due_at"]),("application_documents",["application_id"]),("application_events",["application_id","event_type"])]:op.create_index("ix_"+table+"_lookup",table,cols)
def downgrade():
 for table in ["application_events","application_documents","application_tasks","applications"]:
  op.drop_index("ix_"+table+"_lookup",table_name=table);op.drop_table(table)
