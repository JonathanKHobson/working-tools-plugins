# Exploratory (Global) Research

## Contents

- When
- Mindset
- Steps (originating sources, expert survey, observe)
- Subject focus
- During collection
- Output template
- Filled mini-example
- Benchmarks and statistics
- Risk

## When

- Zero or near-zero prior knowledge of the task, domain, or ecosystem
- Evaluating a new product category, research field, method, vendor, language, framework, or career/domain shift
- Choosing among options before committing (for example: shortlisting products, selecting a study design, or picking a stack for a greenfield project)

## Mindset

Approach without prejudice. Do **not** grant canonical status to experience from adjacent domains.

## Steps

### 1. Study originating sources

- Read originating sources (rank 1) and authoritative references (rank 2), then inspect the thing itself (rank 3) when available
- On conflict: treat the originating source as the record of intended behavior; seek clarification (issues, changelogs, manufacturer notices, errata); do not pick the convenient source. Record intended behavior and reproducible observed behavior separately when they differ.
- Per domain: software — official docs and source; product — manufacturer spec, manual, recall notice; science — original study, dataset, registry; appliance — service manual and error-code table for the exact model; market — company filings, transcripts, official statistics
- Versions and revisions drift; the originating party remains the authority on intent

### 2. Expert survey

No live interview required. Mine existing expert output (rank 1 when it comes from the originating party, rank 4 otherwise):

- Issue trackers, release notes, manufacturer support notices
- Forums, mailing lists, reviewer communities, Stack Overflow
- Conference talks, RFCs, ADRs from maintainers; clinical guideline committees; analyst reports (rank 4 unless the report is the originating filing)

Search for how practitioners actually use the object/subject, not just marketing claims.

### 3. Observe and monitor

- Watch real usage: sample repos, production case studies, live listings, installed-base reports, ecosystem maturity signals
- Track version cadence, breaking changes, price movement, recall activity, community health
- Observation means a bounded investigation, not a promise of background monitoring

## Subject focus

Study subjects **in broad strokes** to build object-level understanding, not deep subject mastery yet.

Multiple subjects are valid (e.g., comparing several languages, product models, study designs, or vendors). Apply the same criteria and the same source ranks to every subject; an uneven comparison is not a comparison.

## During collection

- Append to the findings ledger after every batch; one row per subject per criterion
- Re-check the ledger against the charter questions regularly; volume is high at this stage and drift is easy
- Stop when every criterion has a ledger row for every subject, or is marked *unanswered*

## Output template

```markdown
# [Object] — Exploratory Research

## Charter
[Goal, scope/object/subject(s), type, questions, sources]

## Canonical sources
| Rank | Source | Used for |
|------|--------|----------|

## Glossary
| Term | Definition |
|------|------------|

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|

## Subject descriptions
### [Subject A]
…

## Comparison table
| Criterion | Subject A | Subject B | … |
|-----------|-----------|-----------|---|

## Scope filter
…

## Object filter
…

## Conclusions
[Strategic or production decision with rationale and ledger refs]

## Milestones / Next steps
1. …

## Risks / Unanswered
- …
```

## Filled mini-example

### Task A: choose a serialization format for a new internal RPC layer

```markdown
## Charter
- Goal: pick one wire format for service-to-service RPC; decision must be defensible on latency, schema evolution, and tooling
- Scope / Object / Subject: inter-service communication / RPC payload encoding for this platform / Protobuf, JSON, MessagePack
- Type: exploratory — team has no production experience with binary formats
- Questions: Q1 schema evolution rules; Q2 codegen for Go and TypeScript; Q3 payload size on our typical message
- Sources: protobuf.dev (2), msgpack spec (2), RFC 8259 (2), protobuf GitHub issues (1), local benchmarks (3)

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|
| F1 | Protobuf field numbers must never be reused | protobuf.dev/programming-guides/proto3#updating | 2 | Q1 |
| F2 | MessagePack has no built-in schema; evolution is app-defined | msgpack.org/spec, "Type system" | 2 | Q1 |
| F3 | Our 2 KB JSON message is 640 B in Protobuf | local bench, commit a1b2c3, 10k msgs | 3 | Q3 |

## Scope filter
Nothing discarded — all rows concern encoding, not transport or auth.

## Object filter
Revised F3: measured on one message shape; marked as indicative, not general.

## Conclusions
- Protobuf (F1, F2, F3): explicit evolution rules and codegen for both languages.

## Risks / Unanswered
- Q2 for TypeScript only partially verified (docs, no trial build).
```

### Task B: shortlist three robot vacuums under a budget with pets and hard floors

```markdown
## Charter
- Goal: name three models that meet budget, pet hair, and hard-floor constraints, with evidence per criterion
- Scope / Object / Subject: consumer robot vacuums / models sold in this market under the stated budget / Model A, Model B, Model C
- Type: exploratory — buyer has not used this category
- Questions: Q1 runtime on hard floors; Q2 pet-hair pickup claims vs independent tests; Q3 open recalls or safety notices
- Sources: manufacturer spec sheets (1), regulator recall database (2), live retailer listings with capture date (3), user reviews (4)

## Findings ledger
| # | Claim | Evidence | Rank | Answers |
|---|-------|----------|------|---------|
| F1 | Model A lists 180-minute runtime on hard floors | manufacturer spec sheet, Model A, captured 2026-09-18 | 1 | Q1 |
| F2 | No open recall for Model B in the national consumer-safety database | regulator recall search, Model B, captured 2026-09-18 | 2 | Q3 |
| F3 | Model C is listed at 249 USD from seller S | live listing URL, captured 2026-09-18 14:00 | 3 | Q1 |

## Scope filter
Discarded review-score averages (rank 4) as the only pickup evidence — they do not establish pet-hair performance.

## Object filter
Revised F1: manufacturer runtime is a lab figure; marked as intended spec, not household observation.

## Conclusions
- Shortlist A, B, C on documented runtime, absence of recall, and in-budget live price (F1, F2, F3). Independent pet-hair tests remain unanswered.

## Risks / Unanswered
- Review authenticity not verified; live prices can change after capture.
```

## Benchmarks and statistics

Use benchmarks only when they map to **actual task constraints**.

Reject metrics that look impressive but do not affect the decision (e.g., fast JSON parsing when the protocol is Protobuf, or peak suction when the floor is hard and the constraint is runtime). Do not invent deadlines or effort estimates. If a benchmark does not match the target workload, hardware, dataset, and version, label transferability as uncertain.

## Risk

Skipping pyramid steps here increases the chance of a costly rewrite or a purchase that fails the actual constraints. Treat option selection as a full pyramid run, not a quick blog-post or review-star read.
