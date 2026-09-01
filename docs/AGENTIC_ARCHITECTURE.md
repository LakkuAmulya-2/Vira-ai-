# Vira AI Agentic Architecture

## Why multi-agent

The product contains distinct domains with different policies:

- career guidance
- admissions
- scholarships
- entrance exams
- verified research
- recommendation explanation

A single unrestricted agent is not appropriate.

## Supervisor pattern

```
                    Supervisor
                        │
      ┌────────┬────────┼────────┬─────────┐
      ▼        ▼        ▼        ▼         ▼
   Career   Admission Scholarship Exam  Research
      │        │        │        │         │
      └────────┴────────┼────────┴─────────┘
                        ▼
               Tool / MCP Gateway
                        ▼
              Verified Knowledge Layer
```

## Agent rules

1. Supervisor owns routing.
2. Specialists cannot call arbitrary tools.
3. Tools have typed schemas.
4. Research output is not automatically published as truth.
5. Recommendations retain evidence.
6. Long-running work belongs to workers.
7. Agent execution is bounded and auditable.
8. High-impact actions require confirmation.

## Recommended evolution

Phase 1: deterministic supervisor and specialist contracts.
Phase 2: provider abstraction and structured LLM outputs.
Phase 3: durable workflow orchestration.
Phase 4: asynchronous workers and human approval queues.
Phase 5: MCP gateway for approved integrations.

This avoids premature framework lock-in while preserving a production-grade architecture.
