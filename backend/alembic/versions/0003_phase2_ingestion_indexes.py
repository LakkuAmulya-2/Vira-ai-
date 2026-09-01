"""phase 2 ingestion indexes
Revision ID: 0003_phase2_ingestion_indexes
Revises: 0002_phase1_global_education
Create Date: 2026-09-01
"""
from alembic import op
revision="0003_phase2_ingestion_indexes"
down_revision="0002_phase1_global_education"
branch_labels=None
depends_on=None

def upgrade():
    op.create_index("ix_source_documents_source_hash","source_documents",["source_id","content_hash"],unique=False)
    op.create_index("ix_knowledge_claims_source_document","knowledge_claims",["source_id","document_id"],unique=False)
    op.create_index("ix_education_facts_entity_field_status","education_facts",["entity_type","entity_id","field","status"],unique=False)

def downgrade():
    op.drop_index("ix_education_facts_entity_field_status",table_name="education_facts")
    op.drop_index("ix_knowledge_claims_source_document",table_name="knowledge_claims")
    op.drop_index("ix_source_documents_source_hash",table_name="source_documents")
