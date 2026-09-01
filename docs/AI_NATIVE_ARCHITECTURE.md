# AI-Native Production Architecture

## Core rule

AI is a first-class system layer, but deterministic business logic remains authoritative.

```
Student Context
      ↓
AI Orchestrator
(intent → plan → tools → retrieval → reasoning)
      ├───────────────┬────────────────┐
      ↓               ↓                ↓
Domain Tools      Knowledge RAG     Policies
      ↓               ↓                ↓
Careers / Exams    Verified facts   Approval gates
Colleges / Aid     Freshness        Audit rules
      └───────────────┴────────────────┘
                      ↓
       Structured Recommendation Output
                      ↓
             Explain / Ask Approval
                      ↓
                  Action + Audit
```

## Hybrid recommendation engine

1. Hard eligibility filter
2. Constraint and preference filtering
3. Weighted deterministic scoring
4. Supporting evidence retrieval
5. LLM reasoning and explanation
6. JSON-schema output validation

## Autonomous workflow

```
Observe → Detect → Evaluate → Recommend → Prepare
      → Ask for approval → Execute → Audit
```

No high-impact external action is performed without explicit user approval and policy checks.

## Required guardrails

- structured outputs
- prompt/version registry
- tool allowlists
- PII-aware logging
- source provenance
- freshness metadata
- recommendation audit records
- evaluation datasets
- provider fallback
- human override paths

## Critical data model

Every material education fact should support:

```
source_id
source_url
jurisdiction
verified_at
valid_from
valid_until
confidence
verification_status
```
