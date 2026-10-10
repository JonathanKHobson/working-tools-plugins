# Descriptive (Detailed) Research

## Contents

- When
- Orientation
- Steps (selective survey, expert survey, statistical data)
- Output template
- Filled mini-example
- Quality bar
- Relation to exploratory
- Project pattern

## When

- Object is generally understood; subject details are needed
- Producing a plan, protocol, timeline, requirements or purchase spec, literature-review protocol, or implementation spec

Typical trigger: the option or object is chosen; now define **how** to apply it to a specific feature, purchase, protocol, or milestone.

This is a specification workflow; no implementation or execution is implied.

## Orientation

Forward-looking and theoretical: describes intended implementation; no working artifact required yet.

## Steps

### 1. Selective survey

Study **only** the parts of the object required for the task.

- Exploratory research read whole docs; descriptive research reads targeted sections (configuration, APIs, integration points, listing terms, inclusion criteria, edge cases)
- Leverage the existing theoretical base: go deep on what will be applied, skip the rest
- For every external contract, standard, dosage, tolerance, or listing term you rely on, add one ledger row with the rank 1–2 source that confirms it for the version, model, or population you actually use

### 2. Expert survey (best practices)

Focus on **how to solve the specific task**, not general orientation.

- Patterns, gotchas, recommended architectures for this use case
- Failure mode: poor exploratory work surfaces here as unexpected blockers. If a fundamental keeps coming up unknown, stop and run exploratory on that gap.

### 3. Statistical data collection

Gather **repeatable** metrics:

- Implementation or protocol steps with time estimates only when justified by comparable work
- Benchmarks under conditions matching production (same hardware profile, data size, concurrency, population, workload)
- Results must be reproducible and correlate across runs

Unavailable measurements are not invented. If testing is unavailable, specify the protocol and identify it as not executed.

## Output template

```markdown
# [Feature / Milestone] — Descriptive Research

## Charter
[Goal, scope/object/subject, type, questions, sources]

## Canonical sources
| Rank | Source | Used for |
|------|--------|----------|

## Terms and definitions
| Term | Definition |
|------|------------|

## Prerequisites
- Exploratory conclusions relied upon: …

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|

## Scope filter
…

## Object filter
…

## Implementation / protocol steps
1. [Step] — estimate: … — files/areas: … — based on: F…
2. …

## Acceptance criteria
- [ ] …

## Risks and mitigations
| Risk | Mitigation |
|------|------------|

## Benchmarks / estimates
| Metric | Value | Conditions |
|--------|-------|------------|
```

## Filled mini-example

### Task A: make end-of-step notifications fire on Android in a Capacitor app

```markdown
## Charter
- Goal: a plan whose steps, once applied, make scheduled notifications appear on a Pixel emulator
- Scope / Object / Subject: Android notification delivery / Capacitor LocalNotifications pipeline in this app / `notificationIdFor()`, `scheduleNotifications()`, plugin id validation
- Type: descriptive — pipeline already mapped by a prior experimental report; need exact changes
- Questions: Q1 why the plugin rejects our ids; Q2 which schedule options produce RTC_WAKEUP; Q3 which tests must change
- Sources: @capacitor/local-notifications 8.3.1 Kotlin source (3), its CHANGELOG (1), capacitorjs.com docs (2), project tests (3)

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|
| F1 | Plugin throws OS-PLUG-LNOT-0009 when id > Int.MAX_VALUE | LocalNotification.kt:131 | 3 | Q1 |
| F2 | `notificationIdFor` returns `hash >>> 0`, i.e. up to 2^32-1 | src/services/native/local-notifications.ts:42 | 3 | Q1 |
| F3 | `allowWhileIdle: true` selects setExactAndAllowWhileIdle | capacitorjs.com/docs/apis/local-notifications#schedule | 2 | Q2 |

## Scope filter
Nothing discarded — rows are about Android scheduling constraints that hold for any Capacitor app.

## Object filter
Nothing discarded — F1–F3 all target the exact plugin version pinned in package.json.

## Implementation / protocol steps
1. Clamp ids to `hash & 0x7fffffff` — 15 min — local-notifications.ts — based on: F1, F2
2. Pass `allowWhileIdle: true` in every schedule call — 10 min — based on: F3

## Acceptance criteria
- [ ] `LocalNotifications.schedule` resolves without OS-PLUG-LNOT-0009 in logcat
- [ ] Notification appears in the shade within 3 s of the step end while the app is backgrounded
```

### Task B: PubMed literature-review protocol for intermittent fasting and HbA1c

```markdown
## Charter
- Goal: a protocol that another reviewer could execute to extract design, n, and HbA1c outcome from included trials
- Scope / Object / Subject: nutrition and metabolic health / effect of intermittent fasting on HbA1c in adults with type 2 diabetes / randomized trials and meta-analyses from PubMed, 2015 to date
- Type: descriptive — the question and population are already chosen; need inclusion rules and extraction steps
- Questions: Q1 PICO and search string; Q2 inclusion/exclusion; Q3 what each included record must yield
- Sources: PubMed search syntax (2), PRISMA 2020 (2), ADA or equivalent guideline (2), candidate PMIDs (1)

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|
| F1 | PICO: adults with T2D; intermittent fasting; usual diet or other diet; HbA1c | protocol draft, constrained to user question | 3 | Q1 |
| F2 | PubMed query uses MeSH Diabetes Mellitus, Type 2 AND intermittent fasting, 2015–present, RCT and meta-analysis filters | PubMed Help, search history export | 2 | Q1 |
| F3 | One candidate RCT reports design, n=74, HbA1c change | PMID 12345678, parallel-group RCT | 1 | Q3 |
| F4 | ADA Standards discuss medical nutrition therapy, not this exact fasting protocol | ADA Standards of Care, current year | 2 | Q2 |

## Scope filter
Discarded animal and healthy-volunteer studies — they are outside the stated population.

## Object filter
Revised F4: the guideline does not answer the fasting comparison; kept as context, not as an included trial.

## Implementation / protocol steps
1. Run the exported PubMed query; save PMIDs and retrieval date — based on: F2
2. Screen title/abstract against PICO; exclude non-RCT/non-meta-analysis — based on: F1, F2
3. For each included record extract design, n, intervention, comparator, HbA1c change, funding, retraction status — based on: F3
4. Do not send personal health details to public search; label conclusions as literature summary, not medical advice — based on: source strategy

## Acceptance criteria
- [ ] Every included trial has design, n, and HbA1c outcome extracted
- [ ] Each extraction row cites a PMID or DOI actually opened
- [ ] Exclusions are listed with a reason
```

## Quality bar

The output must be an **implementation-ready spec**: sufficient for execution without further discovery. A person given only this document should be able to carry out the work (code, protocol, purchase check, or review extraction).

Include: terminology, key implementation stages, and measurable completion criteria. Every implementation or protocol step names the ledger rows it rests on; a step without a row is a guess and must be labeled as such. Readiness is conditional if a blocking decision remains unresolved. Do not claim readiness merely because a template is complete.

## Relation to exploratory

Good exploratory research → precise descriptive research.

If descriptive work keeps hitting unknown fundamentals, stop and run (or re-run) exploratory on the gap.

## Project pattern

After global exploratory option selection, **each milestone** gets its own descriptive spec with evaluation criteria. Include deadlines only when they are justified; do not invent them.
