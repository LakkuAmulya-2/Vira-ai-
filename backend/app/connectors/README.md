# Connectors

Phase 2 connectors perform network retrieval and hand content to the ingestion pipeline. They do not treat fetched pages as trusted facts.

Production connector rules:
- use registered/approved sources,
- honor source access policies,
- apply per-source rate limits before scaling,
- preserve URL and content hash provenance,
- skip unchanged documents,
- route extracted facts through verification.
