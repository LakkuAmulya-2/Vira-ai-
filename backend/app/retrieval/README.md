# Phase 4 Retrieval

Verified KnowledgeClaim -> canonical retrieval content -> embedding index -> lexical + semantic scoring -> citation-backed grounded context.

Only VERIFIED claims from VERIFIED sources are eligible. Embedding metadata stores model, dimensions and content hash for safe re-indexing.

The default deterministic local embedding avoids hidden provider dependencies; production deployments can replace it behind the same indexer interface and re-index safely.
