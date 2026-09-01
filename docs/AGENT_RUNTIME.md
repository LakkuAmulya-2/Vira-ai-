# Vira Agent Runtime

## Production execution path

```
API Request
  ↓
Workflow State
  ↓
Supervisor Planning
  ↓
Bounded Parallel Specialists
  ↓
Typed Tool Calls
  ↓
MCP Gateway (allowlisted)
  ↓
Verified Knowledge / External Integrations
  ↓
Evidence + Audit Events
  ↓
Supervisor Synthesis
```

## Current implementation

The repository now contains the production boundary for:

- deterministic supervisor routing
- specialist agent contracts
- bounded async runtime
- execution timeout
- typed workflow state
- AI provider abstraction
- MCP request/response contracts
- MCP allowlist gateway
- domain workflow entry point
- agent runtime tests

## Deliberate safety boundary

An LLM provider is **not hardcoded**. Provider credentials and models belong to deployment configuration, and production adapters should implement structured outputs and tool schemas.

## Next implementation

1. durable workflow persistence
2. Redis-backed queues
3. OpenTelemetry traces
4. real verified-knowledge tools
5. provider adapter
6. human approval queue
7. admission timeline workflow
