# MCP Integration Boundary

MCP is used as an integration protocol, not as an unrestricted agent privilege.

Production architecture:

```
Agent
  ↓
Internal Tool Contract
  ↓
MCP Gateway / Adapter
  ↓
Allowlisted MCP Server
  ↓
External System
```

Recommended server categories:

- document retrieval
- official education data providers
- internal knowledge search
- calendar/deadline systems
- application document storage

Every MCP server must have:

- explicit allowlist
- least-privilege credentials
- timeout
- schema validation
- audit logging
- environment isolation

Do not expose shell, arbitrary network, database administration or secrets tools to agents.
