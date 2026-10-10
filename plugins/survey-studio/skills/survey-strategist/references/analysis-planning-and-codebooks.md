# Analysis Planning and Codebooks

## Plan before fielding

An analysis plan prevents collecting unusable variables and reduces post-hoc storytelling. It should specify:

- decision and primary research questions;
- unit of analysis and denominator;
- primary/secondary metrics;
- hypotheses or descriptive goals;
- comparison groups and covariates;
- sampling/weighting approach;
- exclusions and quality flags;
- missing-data treatment;
- scale scoring and reverse coding;
- open-text coding and adjudication;
- uncertainty and multiplicity handling;
- decision rules and reporting format.

## Question-to-analysis map

| Question ID | Construct | Stored values | Planned statistic/model | Denominator | Decision use |
|---|---|---|---|---|---|
| task_ease | perceived task ease | 1–7 | distribution, median/mean if justified | task completers | identify experience regression |
| obstacle | primary obstacle | coded category | share by category | people reporting difficulty | prioritize investigation |
| explanation | diagnostic verbatim | text | thematic coding | respondents answering item | reveal mechanisms/examples |

Every primary metric must map to a question or trusted record. Every question must map to an analysis, eligibility rule, operational action, or required disclosure.

## Denominators

Record whether percentages use all invited, eligible starts, question viewers, valid answers, or completed surveys. Logic and item nonresponse change denominators. Never hide a small base behind a percentage.

## Missingness

Distinguish at least:

- not shown due to logic;
- optional item skipped;
- prefer not to answer;
- don’t know/not applicable;
- survey breakoff;
- technical failure;
- invalidated/quality exclusion.

Do not recode all missing states to zero or collapse them without justification.

## Multi-select

Specify whether results report respondent percentage, selection percentage, or average selections. Respondent percentages can sum above 100%. Store stable choice codes and make exclusive options detectable.

## Scale scoring

Document item wording/version, value direction, reverse-scored items, minimum data required, aggregation rule, transformations, category thresholds, and benchmark source. Do not change labels or point counts and claim historical comparability without evidence.

## Open-text coding

Define:

- coding unit (response, sentence, incident);
- initial codebook source;
- inductive vs deductive process;
- multi-coding rules;
- sensitive/redaction handling;
- coder training and adjudication;
- whether frequencies are descriptive or representative;
- how quotes are selected and de-identified.

Automated clustering or LLM coding needs a human-reviewed codebook, validation sample, error analysis, privacy review, and versioned prompts/models where relevant.

## Codebook minimum fields

- survey and version;
- block and question ID/export tag;
- respondent-facing label;
- question type and required status;
- choice/row/column code and label;
- scale min/max/anchors;
- logic and validation;
- construct, rationale, analysis use;
- PII/sensitive flag;
- missing-value definitions;
- source/validated measure;
- notes and platform mapping.

Generate with `scripts/generate_codebook.py`. Freeze and version the codebook with the fielded instrument.

## Statistical caution

Match inference to sample design. Report uncertainty and practical significance, not only p-values. Avoid slicing many small subgroups until a dramatic difference appears. Weighting and regression cannot guarantee repair of severe coverage, nonresponse, or measurement bias.
