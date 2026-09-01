# Production Folder Structure

Vira starts as an AI-native modular monolith with explicit domain boundaries.

```
Vira-ai-/
├── .github/workflows/        # CI, tests, security
├── docs/                     # architecture and ADRs
├── prisma/                   # schema, migrations, seeds
├── public/
├── scripts/                  # imports and source verification
├── src/
│   ├── app/                  # Next.js route groups + API
│   │   ├── (marketing)/
│   │   ├── (auth)/
│   │   ├── (student)/
│   │   ├── (parent)/
│   │   ├── (admin)/
│   │   └── api/
│   ├── ai/
│   │   ├── agents/
│   │   ├── orchestrators/
│   │   ├── tools/
│   │   ├── prompts/
│   │   ├── retrieval/
│   │   └── evaluation/
│   ├── components/
│   │   ├── ui/
│   │   ├── layouts/
│   │   └── shared/
│   ├── config/
│   ├── lib/
│   │   ├── auth/
│   │   ├── db/
│   │   ├── cache/
│   │   ├── queue/
│   │   └── logger/
│   ├── modules/
│   │   ├── identity/
│   │   ├── students/
│   │   ├── careers/
│   │   ├── courses/
│   │   ├── exams/
│   │   ├── colleges/
│   │   ├── scholarships/
│   │   ├── recommendations/
│   │   ├── applications/
│   │   ├── documents/
│   │   ├── notifications/
│   │   └── knowledge/
│   ├── server/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── policies/
│   │   ├── jobs/
│   │   └── events/
│   └── types/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
└── workers/
    ├── deadline-monitor/
    ├── source-verifier/
    ├── recommendation-refresh/
    └── notification-dispatcher/
```

## Domain module convention

```
modules/careers/
├── domain/          # types, rules, schemas
├── application/     # use cases and services
├── infrastructure/  # repositories/providers
├── presentation/    # actions and UI adapters
└── index.ts
```

This keeps business logic independent from UI and allows AI tools and background workers to reuse the same application services.
