## Instrument contract

Use [survey.schema.json](../../skills/survey-strategist/assets/survey.schema.json) and [survey-template.yaml](../../skills/survey-strategist/assets/survey-template.yaml) for non-trivial work. Every question must include:

- stable `id` and, when needed, platform `export_tag`;
- type, respondent-facing text, required/optional status;
- rationale, construct, and analysis use;
- coded choices or fully anchored scale;
- display/skip logic, validation, sensitivity, PII, and platform notes when relevant.

Keep respondent copy separate from researcher notes. Do not show rationales or analysis instructions in respondent-facing exports.
