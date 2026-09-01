# Vira Agent Runtime

Phase 5 adds:

Student request -> Supervisor routing -> explicit task plan -> least-privilege tool calls -> grounded retrieval -> specialist execution -> evidence validation -> confidence scoring -> persistent execution trace.

The runtime is provider-agnostic. Deterministic routing remains a safe fallback. Future LLM planning should be introduced behind the planner interface without unrestricted database or network access.
