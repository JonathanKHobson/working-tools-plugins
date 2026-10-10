---
name: survey-strategist
description: Use when a user needs to design, revise, audit, test, program, document, or export a survey, questionnaire, feedback form, screener, poll, intake form, research instrument, or Qualtrics survey; select question types or scales; plan sampling, consent, analysis, or localization; reduce bias and burden; or validate survey files and response-data exports.
---

# Survey Strategist

## Core principle

Build the shortest instrument that can support a real decision with trustworthy data. Trace every item from **decision → construct → question → coded value → analysis use**. Remove any question that cannot complete that chain.

## Non-negotiable distinctions

- Use surveys for standardized measurement across people. Use interviews, observation, diary studies, or usability sessions when the primary need is depth, context, explanation, or discovery. Combine methods when one method cannot resolve the decision.
- Distinguish a **survey instrument** from **response data**. A questionnaire definition, printable form, Qualtrics import file, codebook, and respondent export solve different problems.
- Treat the canonical JSON/YAML instrument as the source of truth. Generate presentation and platform formats from it; do not maintain divergent copies by hand.
- Plan analysis before writing questions. Do not collect “interesting” data without a stated use.
- Never claim anonymity when identifiers, links, IP addresses, contact details, or re-identifiable combinations are collected.
- Do not invent legal compliance, validated-scale status, benchmark comparability, or platform syntax. Flag unresolved constraints.

## Route the request

Survey Studio owns survey design, implementation and exports. Research Methodology and UX Design Toolkit refer here while retaining research framing and interaction review. Adapt this broad workflow to the user's decision; examples from a particular course, workshop, product or service do not establish a separate skill or universal question count. Keep one canonical instrument in its owning project.

| Request | Primary route | Read first |
|---|---|---|
| Create a survey, form, questionnaire, or screener | Create workflow | [workflow-create.md](../../../skills/survey-strategist/references/workflow-create.md) |
| Audit or improve an existing instrument | Audit workflow | [workflow-audit.md](../../../skills/survey-strategist/references/workflow-audit.md) |
| Build or import a Qualtrics survey | Qualtrics workflow | [workflow-qualtrics.md](../../../skills/survey-strategist/references/workflow-qualtrics.md) |
| Choose survey vs interview or mixed methods | Method selection | [method-selection-and-triangulation.md](../../../skills/survey-strategist/references/method-selection-and-triangulation.md) |
| Select question types, scales, or response options | Question architecture | [question-types.md](../../../skills/survey-strategist/references/question-types.md), [response-options-and-scales.md](../../../skills/survey-strategist/references/response-options-and-scales.md) |
| Create a feedback or product survey | Feedback workflow | [feedback-surveys.md](../../../skills/survey-strategist/references/feedback-surveys.md) |
| Implement survey collection or connect multiple entry paths | Implementation | [survey-implementation.md](../../../skills/survey-strategist/references/survey-implementation.md) |
| Export or convert an instrument | Export router | [export-selection.md](../../../skills/survey-strategist/references/export-selection.md) |
| Export or analyze collected responses | Response-data route | [response-data-exports.md](../../../skills/survey-strategist/references/response-data-exports.md) |
| Validate accessibility, privacy, or ethics | Risk review | [accessibility-and-inclusive-design.md](../../../skills/survey-strategist/references/accessibility-and-inclusive-design.md), [privacy-ethics-and-compliance.md](../../../skills/survey-strategist/references/privacy-ethics-and-compliance.md) |

## Default workflow

1. **Frame the decision.** State the decision owner, decision deadline, target population, relevant experience window, and what action changes at each plausible result.
2. **Choose the method.** Confirm that a standardized questionnaire can answer the objective. Recommend interviews or triangulation when respondents must explain context or unknown problems.
3. **Write the analysis plan.** Define primary metrics, segments, exclusions, missing-data handling, open-text coding, sample-size basis, and decision thresholds.
4. **Design the respondent journey.** Start with eligibility and recent behavior; group related items; delay sensitive and demographic items; use branching to hide irrelevant questions.
5. **Draft purposeful questions.** Measure one construct at a time with concise, neutral wording and a bounded timeframe. Prefer closed-ended items for planned comparison and a small number of open-ended items for diagnostic context.
6. **Engineer response options.** Make choices mutually exclusive and collectively sufficient; label scales; include “not applicable,” “prefer not to answer,” or “other” only when conceptually valid.
7. **Audit the instrument.** Run methodological, logic, burden, accessibility, privacy, localization, and export checks. Resolve all errors and justify remaining warnings.
8. **Pretest and pilot.** Test comprehension with target-like participants, verify programming and data shape, then run a small operational pilot before broad fielding when stakes justify it.
9. **Export from one source.** Preserve stable IDs, codes, labels, rationale, and programming notes. Validate the generated format before delivery.
10. **Deliver a complete package.** Include the brief, respondent-facing instrument, rationale/analysis map, programming notes, codebook, QA report, and requested export.

## Intake contract

Infer missing context when low risk. Ask at most one focused question when the answer materially changes the method or instrument. Capture:

- decision and objective;
- target audience, eligibility, geography, language, and mode;
- trigger or experience window;
- desired length and response target;
- required metrics, topics, or validated measures;
- sensitive data, identifiers, incentives, and applicable governance;
- platform, export format, branding, accessibility, and localization needs;
- analysis owner, comparison groups, and decision rules.

Use [survey-brief-template.md](../../../skills/survey-strategist/assets/survey-brief-template.md) when the request is underspecified.

## Instrument contract

Use [survey.schema.json](../../../skills/survey-strategist/assets/survey.schema.json) and [survey-template.yaml](../../../skills/survey-strategist/assets/survey-template.yaml) for non-trivial work. Every question must include:

- stable `id` and, when needed, platform `export_tag`;
- type, respondent-facing text, required/optional status;
- rationale, construct, and analysis use;
- coded choices or fully anchored scale;
- display/skip logic, validation, sensitivity, PII, and platform notes when relevant.

Keep respondent copy separate from researcher notes. Do not show rationales or analysis instructions in respondent-facing exports.

## Quality gates

Do not mark an instrument field-ready until it passes [quality-gates-and-audit-rubric.md](../../../skills/survey-strategist/references/quality-gates-and-audit-rubric.md).

**Release blockers:**

- unclear objective or wrong target population;
- a question without a decision or analysis use;
- leading, double-barreled, ambiguous, or unbounded wording that changes interpretation;
- overlapping choices, missing plausible choices, or an unlabeled scale;
- broken, circular, or forward-referencing logic;
- required sensitive information without necessity and an appropriate skip path;
- privacy notice inconsistent with actual collection;
- inaccessible controls or an unusable mobile layout;
- no pretest for a new or materially changed instrument;
- duplicate IDs/codes or an unvalidated export;
- unsupported platform behavior silently converted or dropped.

## Use the role guides

Use these as focused review passes, not as separate personalities that rewrite one another’s work:

- [Intake strategist](../../../skills/survey-strategist/agents/roles/intake-strategist.md)
- [Methodology advisor](../../../skills/survey-strategist/agents/roles/methodology-advisor.md)
- [Analysis planner](../../../skills/survey-strategist/agents/roles/analysis-planner.md)
- [Question architect](../../../skills/survey-strategist/agents/roles/question-architect.md)
- [Bias and inclusion reviewer](../../../skills/survey-strategist/agents/roles/bias-inclusion-reviewer.md)
- [Accessibility and privacy reviewer](../../../skills/survey-strategist/agents/roles/accessibility-privacy-reviewer.md)
- [Logic and programming reviewer](../../../skills/survey-strategist/agents/roles/logic-programming-reviewer.md)
- [Export engineer](../../../skills/survey-strategist/agents/roles/export-engineer.md)
- [QA auditor](../../../skills/survey-strategist/agents/roles/qa-auditor.md)

## Deterministic tools

Run commands from the skill directory.

```bash
# Validate canonical structure while loading
python scripts/survey_io.py  # library module; use through the commands below

# Methodological and structural audit
python scripts/survey_lint.py examples/product-experience-pulse.yaml --include-info

# Estimate respondent burden and identify hotspots
python scripts/estimate_burden.py examples/product-experience-pulse.yaml

# Generate a coded analysis dictionary
python scripts/generate_codebook.py examples/product-experience-pulse.yaml output/codebook.csv --format csv

# Export one synchronized instrument
python scripts/export_survey.py examples/product-experience-pulse.yaml output/survey.html --format html
python scripts/export_survey.py examples/product-experience-pulse.yaml output/survey.docx --format docx
python scripts/export_survey.py examples/product-experience-pulse.yaml output/survey.pdf --format pdf

# Create and validate Qualtrics TXT
python scripts/export_survey.py examples/product-experience-pulse.yaml output/qualtrics.txt --format qualtrics-advanced
python scripts/validate_qualtrics_txt.py output/qualtrics.txt

# Validate the complete installed skill
python scripts/validate_skill.py .
bash scripts/qa_all.sh
```

Use `--help` for flags. Treat the burden estimate as a planning heuristic, not a promise.

## Qualtrics guardrails

- Prefer **Advanced TXT** for controlled question IDs, blocks, recodes, and supported question types. Read [export-qualtrics-advanced-txt.md](../../../skills/survey-strategist/references/export-qualtrics-advanced-txt.md).
- Use **Simple TXT** only for simple multiple-choice and matrix instruments. Read [export-qualtrics-simple-txt.md](../../../skills/survey-strategist/references/export-qualtrics-simple-txt.md).
- Keep files UTF-8; reject UTF-16.
- Import, inspect every question, program logic/validation not represented by documented tags, preview on desktop/mobile, collect test responses, and inspect exported columns before launch.
- Do not synthesize or hand-edit QSF. Read [export-qualtrics-qsf.md](../../../skills/survey-strategist/references/export-qualtrics-qsf.md).
- Emit explicit warnings for unsupported mappings. Never pass a descriptive placeholder off as a working interactive question.

## Reference library

Read only the files needed for the current request.

### Research strategy and design

- [Reference index](../../../skills/survey-strategist/references/index.md)
- [Survey design foundations](../../../skills/survey-strategist/references/survey-design-foundations.md)
- [Method selection and triangulation](../../../skills/survey-strategist/references/method-selection-and-triangulation.md)
- [Survey types](../../../skills/survey-strategist/references/survey-types.md)
- [Question subject areas](../../../skills/survey-strategist/references/question-subject-areas.md)
- [Question types](../../../skills/survey-strategist/references/question-types.md)
- [Question writing](../../../skills/survey-strategist/references/question-writing.md)
- [Response options and scales](../../../skills/survey-strategist/references/response-options-and-scales.md)
- [Ordering, flow, and logic](../../../skills/survey-strategist/references/ordering-flow-and-logic.md)
- [Sampling, recruitment, and invitations](../../../skills/survey-strategist/references/sampling-recruitment-and-invitations.md)
- [Feedback surveys](../../../skills/survey-strategist/references/feedback-surveys.md)
- [Forms and questionnaires](../../../skills/survey-strategist/references/forms-and-questionnaires.md)
- [Analysis planning and codebooks](../../../skills/survey-strategist/references/analysis-planning-and-codebooks.md)
- [Validated measures](../../../skills/survey-strategist/references/validated-measures.md)

### Risk, quality, and fieldwork

- [Accessibility and inclusive design](../../../skills/survey-strategist/references/accessibility-and-inclusive-design.md)
- [Privacy, ethics, and compliance](../../../skills/survey-strategist/references/privacy-ethics-and-compliance.md)
- [Localization and cross-cultural research](../../../skills/survey-strategist/references/localization-and-cross-cultural-research.md)
- [Pretesting and piloting](../../../skills/survey-strategist/references/pretesting-and-piloting.md)
- [Data quality and fraud](../../../skills/survey-strategist/references/data-quality-and-fraud.md)
- [Quality gates and audit rubric](../../../skills/survey-strategist/references/quality-gates-and-audit-rubric.md)
- [Create workflow](../../../skills/survey-strategist/references/workflow-create.md)
- [Audit workflow](../../../skills/survey-strategist/references/workflow-audit.md)
- [Qualtrics workflow](../../../skills/survey-strategist/references/workflow-qualtrics.md)

### Export and interoperability

- [Export selection](../../../skills/survey-strategist/references/export-selection.md)
- [Markdown export](../../../skills/survey-strategist/references/export-markdown.md)
- [Plain-text export](../../../skills/survey-strategist/references/export-plain-text.md)
- [HTML export](../../../skills/survey-strategist/references/export-html.md)
- [PDF export](../../../skills/survey-strategist/references/export-pdf.md)
- [DOCX export](../../../skills/survey-strategist/references/export-docx.md)
- [JSON export](../../../skills/survey-strategist/references/export-json.md)
- [YAML export](../../../skills/survey-strategist/references/export-yaml.md)
- [XML export](../../../skills/survey-strategist/references/export-xml.md)
- [CSV and TSV export](../../../skills/survey-strategist/references/export-csv-tsv.md)
- [XLSX and XLSForm export](../../../skills/survey-strategist/references/export-xlsx-and-xlsform.md)
- [Qualtrics Simple TXT](../../../skills/survey-strategist/references/export-qualtrics-simple-txt.md)
- [Qualtrics Advanced TXT](../../../skills/survey-strategist/references/export-qualtrics-advanced-txt.md)
- [Qualtrics QSF](../../../skills/survey-strategist/references/export-qualtrics-qsf.md)
- [SurveyJS JSON](../../../skills/survey-strategist/references/export-surveyjs-json.md)
- [REDCap data dictionary](../../../skills/survey-strategist/references/export-redcap-data-dictionary.md)
- [LimeSurvey LSS](../../../skills/survey-strategist/references/export-limesurvey-lss.md)
- [Response-data exports](../../../skills/survey-strategist/references/response-data-exports.md)
- [Limitations and platform caveats](../../../skills/survey-strategist/references/limitations-and-platform-caveats.md)
- [Sources and inspiration](../../../skills/survey-strategist/references/sources.md)

## Output format

Deliver in this order unless the user requests otherwise:

1. **Decision brief** — objective, audience, method choice, assumptions, and missing information.
2. **Instrument** — introduction/consent, blocks, questions, response options, close/thank-you.
3. **Researcher notes** — rationale, construct, analysis use, logic, randomization, validation, and platform programming.
4. **Analysis package** — metrics, coding, exclusions, segments, missing-data handling, and codebook.
5. **QA report** — findings by severity, estimated burden, pretest/pilot status, and unresolved risks.
6. **Requested files** — canonical source plus validated exports and a warning manifest when fidelity is incomplete.

State assumptions and limitations plainly. Legal and compliance material is operational guidance, not legal advice.
