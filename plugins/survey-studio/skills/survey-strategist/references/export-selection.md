# Export Selection

## First identify the artifact class

| Need | Artifact | Typical formats |
|---|---|---|
| Author/edit the instrument | canonical definition | JSON, YAML |
| Review content with stakeholders | researcher-facing document | Markdown, DOCX, PDF |
| Let respondents complete a standalone form | web instrument | accessible HTML or platform-native survey |
| Import into a survey platform | platform definition | Qualtrics TXT, XLSForm, SurveyJS JSON, REDCap dictionary, verified platform format |
| Analyze variable meanings | codebook/data dictionary | CSV, TSV, XLSX, Markdown, JSON |
| Analyze collected responses | response dataset | CSV, TSV, XLSX, JSON/XML, SPSS, database table |
| Archive/transfer a platform survey | platform-native backup | QSF or vendor-specific export produced by the platform |

Do not substitute one class for another. A PDF is not an interactive survey definition; a response CSV is not a questionnaire; a QSF is not response data.

## Source-of-truth policy

Use canonical JSON/YAML as the authoritative instrument when creating multi-format deliverables. Preserve:

- survey and version ID;
- block/question/choice IDs;
- machine values and display labels;
- scale anchors/direction;
- required status, validation, and logic;
- rationale, construct, and analysis use;
- privacy/sensitivity flags;
- platform notes and unsupported-feature warnings.

Generate each derivative, then validate it. Never manually “fix” one derivative without updating the canonical source.

## Fidelity levels

Label each export:

- **Lossless for represented schema:** all canonical fields preserved.
- **Respondent-facing projection:** intentionally omits researcher notes.
- **Review projection:** includes wording/rationale but may not execute logic.
- **Platform mapping:** implements supported features and lists manual work.
- **Presentation only:** appearance for reading/printing; not importable.

## Selection guide

- Choose **JSON** for strict interchange and application integration.
- Choose **YAML** for human-authorable canonical files with validation.
- Choose **Markdown** for version control and content review.
- Choose **HTML** for an accessible standalone prototype; it is not a secure production data system by itself.
- Choose **DOCX** for tracked stakeholder editing.
- Choose **PDF** for fixed visual review, print, or records.
- Choose **XML** when an integration requires XML or a formal standard such as DDI.
- Choose **CSV/TSV** for flat codebooks or response tables.
- Choose **XLSX/XLSForm** for spreadsheet review or ODK-family platform imports.
- Choose **Qualtrics Advanced TXT** for supported Qualtrics question import with explicit tags.

## Universal QA

1. Open/parse the file with an independent reader.
2. Verify encoding and line endings.
3. Compare counts and stable IDs with canonical source.
4. Spot-check labels, codes, scale direction, required status, and logic notes.
5. Confirm unsupported fields are reported, not silently lost.
6. Render visual formats and inspect every page/state.
7. Import platform formats into a nonproduction project and submit test responses.
8. Record generator/version/hash and warning manifest.
