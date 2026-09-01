"""phase 7 recommendation decisions
Revision ID: 0008_phase7_recommendation_decisions
Revises: 0007_phase6_student_intelligence
"""
from alembic import op
revision="0008_phase7_recommendation_decisions";down_revision="0007_phase6_student_intelligence";branch_labels=None;depends_on=None
def upgrade():
    op.create_index("ix_recommendation_runs_student_created","recommendation_runs",["student_id","created_at"])
    op.create_index("ix_recommendation_items_run_score","recommendation_items",["run_id","score"])
def downgrade():
    op.drop_index("ix_recommendation_items_run_score",table_name="recommendation_items");op.drop_index("ix_recommendation_runs_student_created",table_name="recommendation_runs")
