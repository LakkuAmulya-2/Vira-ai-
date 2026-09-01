# Vira Student Intelligence Profile

## Purpose

The Student Intelligence Profile is the shared decision context for Vira's agents and recommendation engine.

## Inputs

- education stage
- academic history
- interests
- strengths
- skills
- career goals
- country preferences
- budget
- constraints

## Output

The system produces:

- normalized profile
- profile completeness score
- missing dimensions
- next best onboarding questions
- versioned profile contract

## Design principle

The first version is deterministic and explainable. AI enrichment should add insights only when the underlying evidence and assumptions are retained.

No fabricated personality traits, aptitude scores, or career predictions are stored as fact.
