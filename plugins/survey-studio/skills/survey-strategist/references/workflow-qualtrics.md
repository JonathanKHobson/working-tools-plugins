# Workflow: Qualtrics Instrument

## Choose the artifact

- **Advanced TXT:** preferred for generated/importable question definitions supported by documented tags.
- **Simple TXT/DOCX:** only for simple multiple-choice/matrix content with limited behavior.
- **QSF:** obtain from Qualtrics for backup/transfer; do not synthesize or hand-edit.
- **Response export:** CSV/TSV/XLSX/XML/SPSS after collection; not an instrument import.

## Build

1. Create and validate canonical JSON/YAML.
2. Ensure stable question IDs/export tags and numeric recodes when required.
3. Keep logic, validation, randomization, quotas, scoring, display, and survey-flow requirements in `platform_notes.qualtrics` and a programming checklist.
4. Generate Advanced TXT:

```bash
python scripts/export_survey.py survey.yaml qualtrics-advanced.txt --format qualtrics-advanced
python scripts/validate_qualtrics_txt.py qualtrics-advanced.txt
```

5. Review the generated warning manifest. Unsupported types become explicit manual-programming placeholders; they are not working equivalents.

## Import

1. Save as UTF-8 plain text; never UTF-16.
2. Import through Qualtrics survey tools into the intended survey/project.
3. Inspect every question type, ID, choice, recode, block, and page break.
4. Program unsupported features in Survey Flow/Look & Feel/question settings.
5. Verify branch/display/skip logic, embedded data, randomization, quotas, scoring, validation, carry-forward, piped text, translations, and termination.

## Test

- desktop/mobile/accessibility preview;
- every path and boundary;
- test distributions/randomization;
- anonymous vs personal-link behavior;
- duplicate prevention, back/save settings, and survey close;
- contact/incentive data separation;
- test responses, labels vs values export, missing/logic values, multi-select columns, dates/time zones, and metadata.

## Handoff

Deliver canonical source, TXT, warning manifest, programming checklist, codebook, path tests, test-response export, and QA report. State the Qualtrics version/date tested and any features that remain manual.
