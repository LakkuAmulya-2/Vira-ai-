# Vira Agent System

## Design

Vira uses a **supervisor-orchestrated, tool-grounded multi-agent architecture**.

Agents do not directly write verified education truth. They produce plans, analyses and explanations. Tools return structured data. Critical facts remain governed by the verified knowledge layer.

## Agents

- SupervisorAgent — routes work, applies policy, controls termination
- CareerAgent — career exploration and pathway reasoning
- AdmissionsAgent — admissions workflow planning
- ScholarshipAgent — scholarship discovery and eligibility workflow
- ExamAgent — entrance exam planning
- ResearchAgent — evidence-oriented research requests
- RecommendationAgent — deterministic ranking + grounded explanation

## Execution model

```
User Request
   ↓
Intent / Risk Classification
   ↓
Supervisor
   ├── direct response
   ├── single specialist
   └── multi-agent plan
           ↓
       Agent calls
           ↓
       Tool results
           ↓
       Supervisor synthesis
           ↓
       Audited response
```

## Production constraints

- bounded recursion and step limits
- explicit agent allowlists
- typed tool contracts
- timeouts and cancellation
- correlation IDs
- audit events
- no autonomous verification of facts
- no direct arbitrary HTTP/database access from agents
- human/admin verification boundary for knowledge publication

MCP servers should be exposed through a gateway and allowlisted by environment. Never give an LLM unrestricted filesystem, shell or network access.
