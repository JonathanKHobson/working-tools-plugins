# Survey Toolkit

Current edition **0.1.3** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Turn a decision and target population into a clear survey instrument, response logic, sampling plan, pilot, export or codebook while preserving question IDs and analysis meaning.

## Start with a real task

| Ask | Bring | You receive |
| --- | --- | --- |
| “Write five neutral questions to measure this experience.” | Decision, population and construct | Questions, response options and coding rationale |
| “Build a survey from this study brief and test its branching.” | Study brief and collection setting | Canonical instrument, flow and testable paths |
| “Export this approved instrument for Qualtrics.” | Canonical instrument and target format | Export, mapping warnings and import verification status |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/survey-strategist/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Use a specialist for a bounded question, sampling, flow, review, export or analysis task. Use survey-strategist for a full instrument or when the method itself is undecided.

| Task / skill | What it produces |
| --- | --- |
| [survey-accessibility-and-privacy](skills/survey-accessibility-and-privacy/SKILL.md) | Review survey consent, sensitive data, accessibility, inclusion and localization against actual collection behavior. |
| [survey-analysis-codebooks](skills/survey-analysis-codebooks/SKILL.md) | Plan survey metrics and create codebooks or response-data exports with stable variable definitions and analysis rules. |
| [survey-export](skills/survey-export/SKILL.md) | Convert a canonical survey into requested documents or platform imports while preserving IDs, codes, logic and known limitations. |
| [survey-flow-and-logic](skills/survey-flow-and-logic/SKILL.md) | Design or debug survey blocks, skip/display logic, validation and collection paths. |
| [survey-pilot-and-quality](skills/survey-pilot-and-quality/SKILL.md) | Audit a survey and plan or evaluate comprehension pretests, operational pilots, burden and data-quality checks. |
| [survey-question-design](skills/survey-question-design/SKILL.md) | Write or revise survey questions, response choices and scales for valid, neutral and analyzable measurement. |
| [survey-sampling](skills/survey-sampling/SKILL.md) | Plan survey population, sampling, recruitment, incentives and response coverage for an explicit research decision. |
| [survey-strategist](skills/survey-strategist/SKILL.md) | Frame a survey decision, choose the research method and coordinate an end-to-end instrument through the appropriate survey specialists. |

## Availability and recovery

This package has no `.mcp.json` or built-in account connection. Its skills and local deterministic helpers use the supplied instrument; platform import, distribution and response access depend on the actual host and account. An exported file is not proof of a successful platform import or collected responses. If a destination is unavailable, deliver the canonical instrument and identify the unverified step.

The [project map](docs/project-map.md) identifies the canonical instrument contract, local helpers and validation. Instruments and respondent data live in their owning projects. Examples are illustrative and need adaptation and pretesting before fielding.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Public edition and prerequisites

This public edition retains all 8 top-level method heads. One restricted supplied QuestionTypes.txt archive excluded; all original procedure/helper content retained. See [source attributions](SOURCE-ATTRIBUTIONS.md), [license](LICENSE), [notices](THIRD_PARTY_NOTICES.md) and [provenance](PROVENANCE.json). No account, provider, data corpus or live connection is installed by this package.

Methods need the decision/population/construct and authorized supplied material. Deterministic helpers need Python 3.10+ and the declared requirements: jsonschema>=4.18, PyYAML>=6.0, python-docx>=1.1, reportlab>=4.0. Install into a reviewed recipient environment; the distribution vendors none of these libraries. Python exporters create caller-selected files; their paths, response privacy and scope need the current task's authorization. Platform accounts/import, real participant data, rendered respondent flow and accessibility acceptance remain separate checks.

Example: “Create and export a brief product-experience pulse.” With no Qualtrics account/provider, finish the canonical synthetic instrument, lint/burden/codebook and supported local export syntax checks, then identify the unverified actual import/flow check. Never claim fielded, anonymous or benchmark-valid from a local file. This is an authored expected scenario, not a recorded live import.

The HTML export is an explicitly labeled review preview with a local required-answer check. It never submits or stores responses; branching and destination rules require a separate implementation. PDF exports are printable review copies, not interactive forms.
