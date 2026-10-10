# PDF Export

## Best for

Fixed-layout stakeholder review, printable questionnaires, records, ethics submissions, and offline reading.

## Not sufficient for

Platform import, reliable interactive data capture, or proof that branching/validation works. Fillable PDF forms require a separate implementation and accessibility test.

Generate:

```bash
python scripts/export_survey.py survey.yaml survey.pdf --format pdf
python scripts/export_survey.py survey.yaml respondent.pdf --format pdf --respondent-only
```

## Layout rules

- show title/version and respondent context;
- keep a question with its options when possible;
- use repeated page headers/footers and page numbers;
- provide ample mark/write space for paper use;
- avoid splitting matrices across pages without repeated headers;
- use tagged/accessible PDF tooling when accessibility is required;
- embed appropriate fonts and preserve selectable text;
- do not convey required status or scale direction by color alone.

## QA

Open with multiple PDF readers, render every page to images, inspect clipping/overflow, page breaks, missing glyphs, links, selectable text, metadata, and print at intended paper size. For accessible PDF, test tags, reading order, headings, form-field labels, and keyboard behavior with specialist tools/users. Record that logic is programming notes only.
