# Workflow: Audit an Existing Instrument

## Inputs

Prefer the exact fielded/programmed version, canonical source or platform export, invitation, consent/privacy text, logic map, codebook, analysis plan, prior results, and target population. When only a screenshot or PDF exists, state which programming/data properties cannot be verified.

## Pass 1 — Purpose and method

- Reconstruct objective, decision, audience, mode, and claims.
- Identify questions with no plausible use and metrics with no source.
- Challenge whether a survey is the right method.

## Pass 2 — Item-level review

For every question record:

- construct and answerability;
- wording defects;
- timeframe/recall;
- response-option coverage/overlap;
- scale anchors/direction;
- sensitivity/PII;
- analysis implications;
- recommended rewrite or deletion.

Do not rewrite before diagnosing; an elegant rewrite cannot rescue an unnecessary construct.

## Pass 3 — Journey and programming

Trace eligibility, common, rare, refusal, missing, randomization, quota, and termination paths. Check required-hidden fields, forward logic, cycles, page context, validation, mobile, accessibility, back/save behavior, and export codes.

## Pass 4 — Sampling and fieldwork

Review sampling frame, invitation, incentive, frequency, response/breakoff, nonresponse, fraud controls, mode effects, and whether reported claims match the design.

## Pass 5 — Privacy, ethics, inclusion, localization

Compare the notice with actual fields/metadata. Review minimization, identifiability, sensitive categories, vulnerable populations, retention/sharing, accessibility, demographic categories, language equivalence, and re-identification.

## Pass 6 — Analysis and files

Review codebook, missing codes, multi-select representation, scale scoring, denominators, exclusions, weights, subgroup sizes, open-text handling, versions, and export integrity.

Run available scripts. For a canonical file:

```bash
python scripts/survey_lint.py survey.yaml --include-info --format json
python scripts/estimate_burden.py survey.yaml --format json
```

## Deliverable

1. Executive verdict and top risks.
2. Rubric score with evidence.
3. Finding table: severity, location, data impact, correction, owner, retest.
4. Revised instrument or patch when requested.
5. Unverifiable properties and required platform tests.
6. Field-ready/ready-after-fixes/not-ready conclusion.
