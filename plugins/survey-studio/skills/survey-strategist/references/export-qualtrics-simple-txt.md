# Qualtrics Simple TXT

## Use only for simple instruments

Simple TXT is appropriate for straightforward multiple-choice and matrix questions. It cannot faithfully represent the full canonical model or complex survey programming.

Generate:

```bash
python scripts/export_survey.py survey.yaml qualtrics-simple.txt --format qualtrics-simple
python scripts/validate_qualtrics_txt.py qualtrics-simple.txt
```

## Documented conventions used

- Separate questions with blank lines.
- Put an export tag followed by a period before question text.
- Put choices below the question with a blank line.
- Use `[[MultipleAnswer]]` below a multiple-answer question.
- Matrix questions contain one group of row statements and one group of scale points separated by a blank line.
- Use `[[Block:Name]]`, `[[PageBreak]]`, and documented randomization tags where supported.
- A question without choices may become descriptive text rather than text entry.

Avoid colons in Simple-format answer labels until after import because Qualtrics may parse them unexpectedly.

## Encoding

Use UTF-8 standard plain text. Qualtrics warns that UTF-16 will not upload correctly. The validator rejects UTF-16.

## Limitations

The exporter maps only supported simple question families and inserts explicit placeholders/warnings for unsupported content. Logic, validation, scoring, translations, quotas, advanced formatting, recodes, and many question types require manual programming after import.

## Import QA

Import into a test survey, inspect every question and choice, replace placeholders, program required behavior, preview paths, submit test responses, and compare exported columns/codes. A passing text validator does not prove Qualtrics executes the intended survey.
