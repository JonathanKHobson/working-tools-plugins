# Response-Data Exports

## Instrument files are not response files

Collected responses should be exported with enough metadata to reproduce analysis. Qualtrics and other platforms commonly offer CSV, TSV, XLSX, XML, SPSS, and API/database paths. Format availability and column conventions vary by platform/version.

## Export choice

- **CSV/TSV:** portable analytical table; handle encoding, quoting, and multi-select columns.
- **XLSX:** convenient human review; risk of type coercion/formulas/row limits.
- **SPSS:** preserves labels and some metadata; verify missing values and encodings.
- **XML/JSON/API:** nested metadata or automation; requires a documented schema.
- **Database/parquet:** preferred for scalable pipelines when platform integration supports it.

## Labels vs values

Export **coded values** for reproducible analysis and retain a codebook. Export **labels** for human review. When possible retain both or a metadata file. Do not analyze localized labels as stable codes.

## Required metadata

- survey/project ID and version;
- response ID and status;
- start/end/recorded timestamps with time zone;
- distribution/source/language/device where authorized;
- question/choice codes and labels;
- logic-skipped vs unanswered states;
- quality/exclusion flags and weights;
- randomization/order/exposure variables for experiments;
- panel/contact linkage key stored separately when possible.

## Multi-select and matrices

Document whether each option becomes a binary column, choice labels are concatenated, or responses are normalized to one row per selection. Matrix columns need row and scale codes. Avoid column names that depend only on display order.

## Data hygiene

1. Export raw immutable data and hash/archive it.
2. Remove test/preview responses with explicit rules.
3. Preserve raw and cleaned datasets separately.
4. Parse dates/numbers with declared locale/time zone.
5. Keep leading zeros and long identifiers as text.
6. Neutralize spreadsheet formula injection for review copies.
7. Redact/minimize identifiers before sharing.
8. Maintain a scripted transformation and data-quality log.

## QA

Compare response counts to platform dispositions, verify every question/path with test responses, inspect labels vs values, missing states, recodes, randomization, weights, text encoding, media/upload links, and time zones. Reconcile the data dictionary before analysis.
