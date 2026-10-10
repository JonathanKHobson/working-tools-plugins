# CSV and TSV Export

## Best for

Flat codebooks, one-row-per-response datasets, analysis-tool interchange, and simple tabular reviews.

Generate a codebook:

```bash
python scripts/generate_codebook.py survey.yaml codebook.csv --format csv
# or
python scripts/export_survey.py survey.yaml codebook.csv --format csv
```

## Instrument vs response table

The provided CSV export is a **codebook**, not a full survey definition. Complex logic, nested blocks, matrices, and form fields cannot be represented cleanly in one flat table without an agreed schema.

## Response-data design

Document:

- one row per respondent/event/answer;
- stable column names tied to question IDs;
- labels vs coded values;
- multi-select representation;
- matrix column naming;
- missing-value codes and skip-by-logic;
- date/time/time zone;
- weights, quality flags, language, version, and source;
- delimiter, quote, newline, and encoding rules.

RFC 4180 describes a common CSV convention, but real tools differ. TSV reduces comma conflicts but still needs escaping rules.

## Security

Neutralize spreadsheet-formula injection for fields beginning with `=`, `+`, `-`, or `@` when files will be opened in spreadsheets, while retaining an unmodified secure analytical source if needed. Never execute macros or formulas from untrusted exports.

## QA

Parse with a CSV library rather than splitting strings; verify row/column counts, quoting, embedded newlines, Unicode, leading zeros, long IDs, formula safety, and round-trip in the intended analytics tool. Do not rely on spreadsheet auto-detection for dates or large numbers.
