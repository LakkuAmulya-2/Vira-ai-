"""phase 5 agent execution
Revision ID: 0006_phase5_agent_execution
Revises: 0005_phase4_retrieval
"""
from alembic import op
import sqlalchemy as sa
revision="0006_phase5_agent_execution"
down_revision="0005_phase4_retrieval"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("agent_executions",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("user_id",sa.String(64),nullable=False),sa.Column("conversation_id",sa.String(64)),sa.Column("status",sa.String(32),nullable=False),sa.Column("primary_agent",sa.String(64),nullable=False),sa.Column("plan",sa.JSON(),nullable=False),sa.Column("final_result",sa.JSON()))
    op.create_table("agent_task_executions",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("execution_id",sa.String(),sa.ForeignKey("agent_executions.id",ondelete="CASCADE"),nullable=False),sa.Column("task_id",sa.String(64),nullable=False),sa.Column("agent",sa.String(64),nullable=False),sa.Column("status",sa.String(32),nullable=False),sa.Column("input",sa.JSON(),nullable=False),sa.Column("output",sa.JSON()),sa.Column("error",sa.Text()),sa.Column("latency_ms",sa.Integer(),nullable=False))
    op.create_index("ix_agent_executions_user_status","agent_executions",["user_id","status"])
    op.create_index("ix_agent_task_executions_execution_status","agent_task_executions",["execution_id","status"])
def downgrade():
    op.drop_index("ix_agent_task_executions_execution_status",table_name="agent_task_executions");op.drop_index("ix_agent_executions_user_status",table_name="agent_executions");op.drop_table("agent_task_executions");op.drop_table("agent_executions")
