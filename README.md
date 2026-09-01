# Vira AI

> **The AI-native Student Decision & Autonomous Admissions Operating System.**

Vira AI helps students move from **confusion → clarity → decision → action → outcome**.

## What Vira solves

- **Career confusion** — personalized career matching and explainable fit.
- **Hidden opportunities** — discover niche careers and courses students may never know exist.
- **Course discovery** — traditional, emerging, vocational and interdisciplinary pathways.
- **Entrance intelligence** — eligibility, exam priorities and deadline tracking.
- **College intelligence** — Dream / Target / Safe recommendations based on fit, budget and constraints.
- **Scholarship intelligence** — profile-based eligibility matching and renewal/deadline tracking.
- **Autonomous admissions** — monitor → detect → recommend → prepare → ask approval → act → audit.

> Vira never silently submits applications or makes legal/financial commitments without explicit user approval.

## Product principles

1. **Decision, not information overload** — answer “What should I do next?”
2. **AI-native, not AI-added** — AI is embedded in discovery, reasoning and proactive workflows.
3. **Grounded critical facts** — eligibility, fees, deadlines and requirements come from verified data.
4. **Explainable recommendations** — show score, reasons, constraints, trade-offs and freshness.

## MVP

```
Student Profile
   ↓
Academic + Interest Intelligence
   ↓
Career Matches + Hidden Opportunities
   ↓
Course Pathways
   ↓
Eligible Entrance Exams
   ↓
College Shortlist
   ↓
Scholarship Matches
   ↓
Next Best Actions
```

### V1 includes
- Authentication and RBAC
- Student onboarding and intelligence profile
- Career discovery
- Hidden course/career discovery
- Hybrid recommendation engine
- Entrance eligibility
- College shortlist
- Scholarship matching
- AI copilot with grounded context
- Deadline notifications

### Not V1
- Fully automatic application submission
- Unverified data presented as authoritative
- Premature microservices
- Global expansion before the India workflow is reliable

## Production stack

| Layer | Choice |
|---|---|
| Web | Next.js + React + TypeScript |
| Styling | Tailwind CSS + accessible primitives |
| Database | PostgreSQL |
| ORM | Prisma |
| Validation | Zod |
| Auth | Auth.js or equivalent |
| Cache / Jobs | Redis + queue worker |
| AI | Provider abstraction + structured outputs + tools |
| Knowledge | Verified structured data + retrieval |
| Storage | S3-compatible object storage |
| Tests | Vitest + Playwright |
| CI/CD | GitHub Actions |

## Architecture

See:
- [Folder structure](docs/FOLDER_STRUCTURE.md)
- [AI-native architecture](docs/AI_NATIVE_ARCHITECTURE.md)
- [System architecture](docs/ARCHITECTURE.md)

## AI recommendation pipeline

```
Student Profile
      ↓
Hard Eligibility Filters
      ↓
Constraints & Preferences
      ↓
Deterministic Scoring
      ↓
Search / Retrieval
      ↓
LLM Reasoning & Explanation
      ↓
Structured Recommendation
      ↓
Student Approval / Action
```

The LLM is an intelligence and explanation layer—not the sole source of truth.

## Local development

```bash
git clone https://github.com/LakkuAmulya-2/Vira-ai-.git
cd Vira-ai-
npm install
cp .env.example .env.local
npm run dev
```

## Environment

```env
NEXT_PUBLIC_APP_URL=http://localhost:3000
DATABASE_URL=
DIRECT_URL=
AUTH_SECRET=
AI_PROVIDER=
AI_API_KEY=
REDIS_URL=
ERROR_TRACKING_DSN=
```

Never commit real secrets.

## Engineering standards

- TypeScript strict mode
- Zod validation at boundaries
- domain/service separation
- thin API routes
- authorization before data access
- idempotent jobs
- structured logs
- audit trails for autonomous actions
- unit/integration/E2E tests
- mobile-first accessibility
- source freshness for critical education data

## Delivery roadmap

- [x] Product architecture
- [x] Premium UI foundation
- [x] Initial onboarding
- [x] Core documentation
- [ ] PostgreSQL + Prisma
- [ ] Authentication + RBAC
- [ ] Student persistence
- [ ] Hybrid recommendation engine
- [ ] Grounded AI copilot
- [ ] Entrance engine
- [ ] College fit scoring
- [ ] Scholarship matching
- [ ] Autonomous monitoring
- [ ] CI, observability and security hardening

## North-star experience

A student should be able to say:

> **“I completed 12th. I don't know what to do next.”**

Vira should understand the student, discover options they may never have heard of, verify eligibility, compare trade-offs, surface opportunities before deadlines, and guide the next best action.
