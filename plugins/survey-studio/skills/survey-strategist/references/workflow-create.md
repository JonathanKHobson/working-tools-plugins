# Workflow: Create a Survey, Form, or Questionnaire

## Phase 1 — Frame

1. Convert the request into a decision brief.
2. Define target population, eligibility, sampling frame, trigger, mode, language, and requested export.
3. Decide whether a survey is appropriate; recommend qualitative or mixed methods when needed.
4. Identify privacy/ethics/accessibility constraints and required reviewers.

**Gate:** no drafting until the objective and audience are coherent.

## Phase 2 — Analyze before asking

1. Complete the analysis plan.
2. Define primary/secondary metrics, segments, exclusions, missingness, open-text coding, and decision rules.
3. Create a question-to-analysis skeleton with stable IDs.

**Gate:** each planned metric has a data source; no unnecessary variables.

## Phase 3 — Architect

1. Design blocks and respondent paths.
2. Draft eligibility and recent-behavior items.
3. Draft primary outcome and diagnostic items.
4. Add sensitive/demographic items only when required.
5. Add introduction, consent/privacy, help, and close.
6. Encode choices, scales, logic, validation, rationale, construct, and analysis use in canonical JSON/YAML.

## Phase 4 — Review

Run focused passes using the role guides:

- methodology and sampling;
- question wording/options/scales;
- bias/inclusion;
- accessibility/privacy/ethics;
- logic/programming;
- analysis/codebook.

Run:

```bash
python scripts/survey_lint.py <survey.yaml> --include-info
python scripts/estimate_burden.py <survey.yaml>
```

Resolve errors and document accepted warnings.

## Phase 5 — Pretest

1. Expert review.
2. Cognitive interviews with target-like respondents.
3. Accessibility and device usability tests.
4. Programmed path tests and test-response exports.
5. Soft launch/pilot when warranted.
6. Revise and version; retest changed areas.

When a working collection flow is requested, use [survey implementation](survey-implementation.md) for persistence, context, access and end-to-end checks. Do not infer a build request from a draft-only task.

## Phase 6 — Export and handoff

1. Generate codebook and requested formats from canonical source.
2. Validate syntax, encoding, file integrity, visual output, and platform import.
3. Include warning manifest/manual programming notes.
4. Deliver brief, instrument, researcher notes, analysis plan, codebook, QA report, and final files.

**Final gate:** apply the quality rubric and issue a field-readiness verdict.
