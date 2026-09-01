# Vira Recommendation Engine

## Design principle

Recommendations are not generated from an LLM alone.

```
Student Profile
   ↓
Verified Knowledge Claims
   ↓
Hard Eligibility Filter
   ↓
Constraint Filter
   ↓
Deterministic Scoring
   ↓
Ranking
   ↓
Evidence Attachment
   ↓
AI Explanation
```

## Current entities

- career
- course
- college
- scholarship

## Knowledge contract

The engine reads only knowledge claims where:

- status = VERIFIED
- entity type matches the requested domain
- field = profile

Each profile claim can contain:

```json
{
  "title": "Example",
  "annual_cost_minor": 0,
  "currency": "USD",
  "attributes": {
    "education_stages": ["AFTER_12"],
    "eligible_countries": ["IN"],
    "interests": ["computer science"],
    "career_goals": ["software engineer"]
  }
}
```

This is a schema contract, not product seed data.

## No dummy truth

The repository intentionally does not insert fake colleges, courses or scholarships. Production data must enter through verified source ingestion.
