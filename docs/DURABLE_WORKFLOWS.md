# Durable Workflows and Autonomous Monitoring

## Production lifecycle

```
API Request
  ↓
Idempotency Key
  ↓
Workflow Run
  ↓
Checkpoint Before Side Effects
  ↓
Background Job
  ↓
Step Result
  ↓
Checkpoint
  ↓
Resume / Retry
  ↓
Completed
```

## Workflow persistence

Workflow runs persist:

- owner
- workflow type
- idempotency key
- status
- current step
- state snapshot
- error
- version
- timestamps

## Autonomous monitoring

The monitoring boundary supports:

- scholarship deadline watches
- application deadline watches
- exam registration watches
- source freshness checks
- change detection

Notification delivery remains a separate adapter so email, push and messaging providers are not coupled to domain logic.

## Deployment recommendation

- PostgreSQL: workflow state and audit records
- Redis: queues and short-lived coordination
- Worker runtime: scheduled and asynchronous execution
- OpenTelemetry: traces and metrics
