"""phase 4 hybrid retrieval
Revision ID: 0005_phase4_retrieval
Revises: 0004_phase3_source_intelligence
"""
from alembic import op
import sqlalchemy as sa
revision="0005_phase4_retrieval"
down_revision="0004_phase3_source_intelligence"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("knowledge_embeddings",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("claim_id",sa.String(),sa.ForeignKey("knowledge_claims.id",ondelete="CASCADE"),nullable=False),sa.Column("model",sa.String(160),nullable=False),sa.Column("dimensions",sa.Integer(),nullable=False),sa.Column("embedding",sa.JSON(),nullable=False),sa.Column("content",sa.Text(),nullable=False),sa.Column("content_hash",sa.String(64),nullable=False),sa.Column("status",sa.String(32),nullable=False),sa.UniqueConstraint("claim_id"))
    op.create_table("retrieval_audits",sa.Column("id",sa.String(),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True)),sa.Column("updated_at",sa.DateTime(timezone=True)),sa.Column("query_hash",sa.String(64),nullable=False),sa.Column("user_id",sa.String(64)),sa.Column("filters",sa.JSON()),sa.Column("result_count",sa.Integer(),nullable=False))
    op.create_index("ix_knowledge_embeddings_status","knowledge_embeddings",["status"])
    op.create_index("ix_retrieval_audits_query_hash","retrieval_audits",["query_hash"])
def downgrade():
    op.drop_index("ix_retrieval_audits_query_hash",table_name="retrieval_audits");op.drop_index("ix_knowledge_embeddings_status",table_name="knowledge_embeddings");op.drop_table("retrieval_audits");op.drop_table("knowledge_embeddings")
