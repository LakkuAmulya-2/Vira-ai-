# Education Knowledge Layer

This layer stores **provenance before recommendations**.

## Trust pipeline

```
Official source
   ↓
DataSource (pending)
   ↓
SourceDocument (pending)
   ↓
KnowledgeClaim (pending)
   ↓
Human/system verification
   ↓
Verified + effective dates
   ↓
Recommendation/read APIs
```

## Rules

- No seed data is included.
- No college, exam, scholarship or deadline is invented.
- Public decision APIs must only consume VERIFIED claims.
- Expired claims are excluded from current reads.
- Every critical fact retains source and document provenance.
- Administrative writes are RBAC-protected and audited.

## Domain entities

- Career
- Course
- College
- Program
- EntranceExam
- Scholarship

These entities are initially created in DRAFT state and must not become recommendation candidates until their supporting facts are verified.

## Claim model

A claim represents one sourced fact, for example:

- eligibility requirement
- deadline
- tuition
- scholarship award
- program availability

Claims are field-level so conflicting facts can be independently reviewed and traced.
