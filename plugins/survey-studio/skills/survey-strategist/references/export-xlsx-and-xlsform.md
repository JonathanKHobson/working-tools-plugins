# XLSX and XLSForm Export

## XLSX

Use XLSX for multi-sheet stakeholder review, formatted codebooks, analysis-ready tables, and workflows that require Excel. Keep raw data, codebook, README/metadata, value labels, and derived calculations on separate sheets. Avoid merged cells in data ranges, hidden logic, volatile formulas, and macros unless explicitly required and reviewed.

Preserve IDs as text, freeze headers, use filters/tables, define date/time zones, and protect formula cells without pretending workbook protection is security.

## XLSForm

XLSForm is a spreadsheet specification used by ODK-family and compatible tools. A typical workbook includes:

- `survey`: type, name, label, hint, required, relevant, constraint, calculation, choice filter, appearance;
- `choices`: list name, value/name, label;
- `settings`: form title, form ID, version, instance name and platform settings.

Mapping requires more than copying question text. Translate canonical types and logic into the exact XLSForm version/platform syntax; verify repeats, groups, calculations, media, languages, audit settings, and identifiers.

The current skill does not generate XLSX/XLSForm automatically. Use the canonical schema plus a verified platform mapping, then test with the target validator and server/app.

## QA

- workbook opens without repair warnings;
- sheet/range names and headers are exact;
- IDs remain text and unique;
- formulas reference correct cells and no errors remain;
- data validation and named ranges work;
- XLSForm passes the target converter/validator;
- form is previewed and test-submitted on target devices;
- exported responses match the codebook.
