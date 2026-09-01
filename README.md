# Vira AI

> **AI-native Student Decision & Autonomous Admissions Operating System.**

Vira AI helps students move from **confusion → clarity → decision → action → outcome**.

## Production architecture

```
Next.js Web / Mobile Clients
            │
            ▼
       FastAPI Backend
            │
   ┌────────┼─────────┐
   ▼        ▼         ▼
Postgres   Redis   AI Orchestration
            │
            ▼
   Verified Education Knowledge
```

### Backend authority

FastAPI is the authoritative backend for:

- authentication boundary and RBAC
- student profiles
- education knowledge
- verified sources and claims
- recommendation engine
- admissions workflows
- scholarships and deadlines
- audit trails
- background jobs

The frontend must not own business-domain persistence.

## Core product flow

```
Student Profile
   ↓
Academic + Interest Intelligence
   ↓
Verified Knowledge Retrieval
   ↓
Hard Eligibility Filters
   ↓
Deterministic Ranking
   ↓
AI Explanation
   ↓
Next Best Action
```

## Production stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + React + TypeScript |
| Backend | FastAPI + Python |
| Database | PostgreSQL |
| Backend ORM | SQLAlchemy 2 Async |
| Migrations | Alembic |
| API validation | Pydantic |
| Auth | JWT/OIDC boundary + RBAC |
| Cache / jobs | Redis + workers |
| AI | Provider abstraction + structured outputs |
| Knowledge | Verified sources + documents + claims |
| Tests | Pytest + Vitest + Playwright |
| CI/CD | GitHub Actions |

## Repository structure

```
backend/
  app/
    api/v1/
    core/
    db/
    models/
    schemas/
    services/
  alembic/
frontend/
docs/
workers/
```

## No dummy data policy

Vira does not ship fake:

- colleges
- scholarships
- entrance deadlines
- eligibility requirements
- career recommendations

Critical education facts require source provenance and verification.

## Backend local development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
alembic revision --autogenerate -m "initial_schema"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

API documentation is available at:

```
http://localhost:8000/docs
```

## Next production phases

1. Complete FastAPI domain migrations
2. JWT/OIDC provider integration
3. Recommendation engine
4. Knowledge ingestion workers
5. Admissions, exam and scholarship modules
6. AI orchestration with grounded retrieval
7. Observability, rate limiting and CI/CD hardening
