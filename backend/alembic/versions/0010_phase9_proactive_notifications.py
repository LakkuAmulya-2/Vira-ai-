"""phase 9 proactive notifications
Revision ID: 0010_phase9_proactive_notifications
Revises: 0009_phase8_applications
"""
from alembic import op
import sqlalchemy as sa
revision="0010_phase9_proactive_notifications";down_revision="0009_phase8_applications";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("student_alerts",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("alert_type",sa.String(80),nullable=False),sa.Column("entity_type",sa.String(80)),sa.Column("entity_key",sa.String(240)),sa.Column("priority",sa.String(24),nullable=False),sa.Column("status",sa.String(32),nullable=False),sa.Column("title",sa.String(400),nullable=False),sa.Column("body",sa.Text(),nullable=False),sa.Column("action_url",sa.String(2048)),sa.Column("payload",sa.JSON(),nullable=False),sa.Column("dedupe_key",sa.String(240),nullable=False,unique=True))
 op.create_table("notification_preferences",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False,unique=True),sa.Column("deadline_alerts",sa.Boolean(),nullable=False),sa.Column("scholarship_alerts",sa.Boolean(),nullable=False),sa.Column("admission_alerts",sa.Boolean(),nullable=False),sa.Column("exam_alerts",sa.Boolean(),nullable=False),sa.Column("channels",sa.JSON(),nullable=False),sa.Column("quiet_hours",sa.JSON(),nullable=False))
 for t,c in [("student_alerts",["student_id","priority","status"]),("notification_preferences",["student_id"])]:op.create_index("ix_"+t+"_phase9",t,c)
def downgrade():
 for t in ["notification_preferences","student_alerts"]:op.drop_index("ix_"+t+"_phase9",table_name=t);op.drop_table(t)
