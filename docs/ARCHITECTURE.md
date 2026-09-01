# Vira AI — Architecture

## Product boundary

Vira owns the decision and orchestration layer around a student's education journey. Critical facts such as eligibility, deadlines, fees and scholarship rules should come from verified structured sources. The LLM explains, compares and personalizes; it must not invent authoritative facts.

## High-level system

```text
Web / Mobile UX
      |
      v
Application Layer
      |
      +--> Student Profile
      +--> Career Intelligence
      +--> Course Intelligence
      +--> Exam Intelligence
      +--> College Intelligence
      +--> Scholarship Intelligence
      +--> Application/Admission Workflow
      |
      v
Recommendation Orchestrator
      |
      +--> Deterministic rules
      +--> Eligibility filters
      +--> Scoring models
      +--> Search / retrieval
      +--> LLM reasoning + explanation
      |
      v
Verified Education Knowledge Base
      |
      +--> source URL
      +--> last verified timestamp
      +--> jurisdiction
      +--> validity period
      +--> confidence/status
```

## AI-native principles

### Grounding first

Any answer containing a material claim about eligibility, dates, fees, scholarship amounts or admissions requirements must be grounded in structured data or cited source material.

### Hybrid recommendations

1. Filter on hard eligibility rules.
2. Score fit against profile constraints.
3. Rank using outcome and preference signals.
4. Use the LLM to explain trade-offs in natural language.

### Autonomous, not uncontrolled

The agent can monitor and prepare work, but submission of applications or legal/financial commitments requires explicit student approval.

```text
Observe → Detect → Recommend → Prepare → Ask for approval → Act → Audit
```

## Core domains

- `students`: profile, academic records, interests, goals, preferences
- `careers`: career taxonomy, pathways, skills, outcomes
- `courses`: programs, eligibility, pathways, outcomes
- `colleges`: institutions, programs, location, costs, outcomes
- `exams`: exams, eligibility rules, registration windows
- `scholarships`: programs, eligibility rules, awards, deadlines
- `applications`: user applications and workflow state
- `documents`: document checklist, metadata, verification status
- `recommendations`: explanations, scores, reasons, confidence
- `notifications`: deadline and proactive guidance
- `ai`: conversations, tool calls, grounded answer context

## Safety and trust

- Protect minor/student data.
- Use strict RBAC.
- Keep audit trails for recommendations and autonomous actions.
- Clearly label sponsored content.
- Show source and freshness for critical education data.
- Allow account deletion and data export.
