# Markdown Export

## Best for

Version control, pull-request review, content collaboration, plain-text archives, and conversion to other documents.

## Not sufficient for

Executing logic, enforcing validation, collecting responses securely, preserving complex visual layout, or representing every platform setting.

## Recommended structure

- metadata and objective;
- introduction/consent;
- blocks and question IDs;
- respondent wording and options;
- optional researcher notes: rationale, construct, analysis use, logic, validation;
- programming warnings and version.

Generate:

```bash
python scripts/export_survey.py survey.yaml survey.md --format markdown
python scripts/export_survey.py survey.yaml respondent.md --format markdown --respondent-only
```

## Conventions

Use headings for blocks, numbered questions, bullet choices, tables only when they remain readable, fenced code for logic expressions, and explicit values when reviewing codes. Keep line wrapping stable for useful diffs. Do not encode required status through color or an unexplained symbol alone.

## QA

Check heading hierarchy, relative links, escaping of pipes/backticks, stable IDs, option order, researcher-note visibility, logic notes, and rendering in the target Markdown engine. Markdown dialects differ; test tables and task-list syntax before relying on them.
