## Qualtrics guardrails

- Prefer **Advanced TXT** for controlled question IDs, blocks, recodes, and supported question types. Read [export-qualtrics-advanced-txt.md](../../skills/survey-strategist/references/export-qualtrics-advanced-txt.md).
- Use **Simple TXT** only for simple multiple-choice and matrix instruments. Read [export-qualtrics-simple-txt.md](../../skills/survey-strategist/references/export-qualtrics-simple-txt.md).
- Keep files UTF-8; reject UTF-16.
- Import, inspect every question, program logic/validation not represented by documented tags, preview on desktop/mobile, collect test responses, and inspect exported columns before launch.
- Do not synthesize or hand-edit QSF. Read [export-qualtrics-qsf.md](../../skills/survey-strategist/references/export-qualtrics-qsf.md).
- Emit explicit warnings for unsupported mappings. Never pass a descriptive placeholder off as a working interactive question.
