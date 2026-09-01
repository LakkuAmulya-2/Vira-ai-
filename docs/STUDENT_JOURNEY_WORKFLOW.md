# Vira Student Journey Workflow

## Flagship workflow

The workflow coordinates the student's complete decision journey:

1. profile intelligence
2. career discovery
3. course discovery
4. college matching
5. scholarship matching
6. exam discovery
7. eligibility analysis
8. budget analysis
9. deadline timeline
10. action plan

## Durable workflow boundary

The orchestration contract is intentionally separated from persistence. Production deployment should persist:

- workflow ID
- state snapshots
- completed steps
- tool calls
- source evidence
- failures
- human review requests

This enables safe resume/retry behavior without rerunning completed side effects.

## Current API

```
POST /api/v1/journey/start
```

The authenticated user becomes the workflow owner.

## Production next steps

- PostgreSQL workflow persistence
- idempotency keys
- Redis queue workers
- step checkpoints
- cancellation
- human approval
- source freshness checks
- notification delivery
