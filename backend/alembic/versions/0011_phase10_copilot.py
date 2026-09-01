"""phase 10 persistent copilot
Revision ID: 0011_phase10_copilot
Revises: 0010_phase9_proactive_notifications
"""
from alembic import op
import sqlalchemy as sa
revision="0011_phase10_copilot";down_revision="0010_phase9_proactive_notifications";branch_labels=None;depends_on=None
def upgrade():
 op.create_table("copilot_conversations",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("title",sa.String(400),nullable=False),sa.Column("status",sa.String(32),nullable=False),sa.Column("context_snapshot",sa.JSON(),nullable=False))
 op.create_table("copilot_messages",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("conversation_id",sa.String(),sa.ForeignKey("copilot_conversations.id",ondelete="CASCADE"),nullable=False),sa.Column("role",sa.String(24),nullable=False),sa.Column("content",sa.Text(),nullable=False),sa.Column("metadata_json",sa.JSON(),nullable=False))
 op.create_table("copilot_actions",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("student_id",sa.String(),sa.ForeignKey("student_profiles.id",ondelete="CASCADE"),nullable=False),sa.Column("conversation_id",sa.String(),sa.ForeignKey("copilot_conversations.id",ondelete="SET NULL")),sa.Column("action_type",sa.String(100),nullable=False),sa.Column("title",sa.String(400),nullable=False),sa.Column("status",sa.String(32),nullable=False),sa.Column("requires_confirmation",sa.Boolean(),nullable=False),sa.Column("payload",sa.JSON(),nullable=False),sa.Column("result",sa.JSON()))
 for t,c in [("copilot_conversations",["student_id","status"]),("copilot_messages",["conversation_id","role"]),("copilot_actions",["student_id","status","action_type"])]:op.create_index("ix_"+t+"_phase10",t,c)
def downgrade():
 for t in ["copilot_actions","copilot_messages","copilot_conversations"]:op.drop_index("ix_"+t+"_phase10",table_name=t);op.drop_table(t)
