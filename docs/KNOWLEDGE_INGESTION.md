# Vira Knowledge Ingestion Pipeline

## Pipeline

```
Approved Source
  ↓
Connector
  ↓
Normalization
  ↓
Candidate Claim
  ↓
Validation
  ↓
Pending Verification
  ↓
Verification Queue
  ↓
Verified Knowledge
  ↓
Recommendation Engine
```

## Source policy

Only approved connectors may ingest data. Connectors should target authoritative sources such as official universities, examination authorities, governments and scholarship providers.

## Truth boundary

Ingestion does not automatically create verified truth.

Every candidate claim must retain:

- source URL
- entity identity
- field
- value
- source type
- country context where applicable

## Production rollout

1. source registry and approval
2. connector implementation
3. asynchronous scheduling
4. candidate claim persistence
5. deduplication
6. change detection
7. verification queue
8. source freshness monitoring
9. audit logs
