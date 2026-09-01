"""Worker entry point for scheduled knowledge ingestion.

Queue implementation is intentionally infrastructure-agnostic. Production deployments
should invoke KnowledgeIngestionWorkflow through an approved worker runtime.
"""
