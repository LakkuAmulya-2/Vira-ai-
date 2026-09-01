# Phase 2 Verified Data Ingestion

Pipeline:

1. Connector fetches a registered source.
2. SourceDocument stores URL, hash, fetch timestamp and parse status.
3. SHA-256 change detection skips unchanged documents unless force=true.
4. Parser extracts readable text and JSON-LD.
5. Extractor produces candidate claims with confidence.
6. Canonicalizer resolves claims against Phase 1 entities.
7. KnowledgeClaim preserves raw provenance.
8. EducationFact is created only when a canonical entity is resolved.
9. Facts remain PENDING until the existing review workflow verifies them.

No source-specific institution data is hardcoded. Source-specific adapters should be added as separate connector implementations, not mixed into canonical models.
