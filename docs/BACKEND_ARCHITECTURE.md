# Vira AI Backend Architecture

## Runtime split

- **Frontend:** Next.js / React
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2 async
- **Migrations:** Alembic
- **Auth boundary:** JWT validation and RBAC
- **Jobs/cache:** Redis-backed worker boundary

## Production rules

1. FastAPI is the authoritative application backend.
2. Frontend does not contain business-domain persistence logic.
3. Every write is validated with Pydantic.
4. Critical education facts require provenance and verification.
5. Recommendation output must retain algorithm version, input snapshot and evidence.
6. No seed data is shipped as product truth.
7. No LLM output is persisted as verified knowledge without source verification.

## API modules

```
/api/v1/students/me/profile
/api/v1/knowledge/sources
/api/v1/knowledge/claims/{id}/verify
```

Next additions should remain modular: admissions, exams, scholarships, recommendations, notifications and AI orchestration.
