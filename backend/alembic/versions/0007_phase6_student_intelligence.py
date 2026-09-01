"""phase 6 student intelligence
Revision ID: 0007_phase6_student_intelligence
Revises: 0006_phase5_agent_execution
"""
from alembic import op
import sqlalchemy as sa
revision="0007_phase6_student_intelligence"
down_revision="0006_phase5_agent_execution"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("student_academic_records",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("qualification",sa.String(120),nullable=False),sa.Column("board_or_system",sa.String(120)),sa.Column("score",sa.Float()),sa.Column("score_scale",sa.Float()),sa.Column("graduation_year",sa.Integer()))
    op.create_table("student_constraints",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("category",sa.String(80),nullable=False),sa.Column("value",sa.Text(),nullable=False),sa.Column("importance",sa.Integer(),nullable=False))
    op.create_table("student_intelligence_snapshots",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("profile_version",sa.String(32),nullable=False),sa.Column("completeness_score",sa.Float(),nullable=False),sa.Column("profile",sa.JSON(),nullable=False),sa.Column("assumptions",sa.JSON(),nullable=False),sa.Column("active",sa.Boolean(),nullable=False))
    op.create_table("student_memories",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("namespace",sa.String(80),nullable=False),sa.Column("memory_key",sa.String(160),nullable=False),sa.Column("value",sa.JSON(),nullable=False),sa.Column("confidence",sa.Float(),nullable=False),sa.Column("source",sa.String(64),nullable=False),sa.Column("expires_at",sa.String(64)),sa.UniqueConstraint("student_id","namespace","memory_key"))
    op.create_index("ix_student_academic_records_student","student_academic_records",["student_id"]);op.create_index("ix_student_constraints_student","student_constraints",["student_id"]);op.create_index("ix_student_intelligence_snapshots_student_active","student_intelligence_snapshots",["student_id","active"]);op.create_index("ix_student_memories_student_namespace","student_memories",["student_id","namespace"])
def downgrade():
    op.drop_index("ix_student_memories_student_namespace",table_name="student_memories");op.drop_index("ix_student_intelligence_snapshots_student_active",table_name="student_intelligence_snapshots");op.drop_index("ix_student_constraints_student",table_name="student_constraints");op.drop_index("ix_student_academic_records_student",table_name="student_academic_records");op.drop_table("student_memories");op.drop_table("student_intelligence_snapshots");op.drop_table("student_constraints");op.drop_table("student_academic_records")
