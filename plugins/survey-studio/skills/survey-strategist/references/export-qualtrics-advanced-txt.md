# Qualtrics Advanced TXT

## Purpose

Advanced TXT explicitly declares question types, subtypes, IDs, choices, recodes, blocks, page breaks, and some embedded data using `[[...]]` tags. It is the preferred generated Qualtrics import format in this skill.

Generate and validate:

```bash
python scripts/export_survey.py survey.yaml qualtrics-advanced.txt --format qualtrics-advanced
python scripts/validate_qualtrics_txt.py qualtrics-advanced.txt
```

The exporter also writes a `.warnings.json` manifest when mappings are incomplete or manual programming is required.

## Core documented tags

- `[[AdvancedFormat]]`
- `[[Block:Block name]]`, `[[PageBreak]]`
- `[[Question:MC:...]]` for multiple choice variants
- `[[Question:Matrix:...]]`
- `[[Question:TE:SingleLine]]`, `[[Question:TE:Essay]]`, `[[Question:TE:Form]]`
- `[[Question:CS]]`, `[[Question:RO]]`, `[[Question:DB]]`
- `[[ID:question_id]]`
- `[[Choices]]`, `[[Answers]]`
- `[[AdvancedChoices]]` with `[[Choice:recode]]`
- `[[AdvancedAnswers]]` with `[[Answer:recode]]`
- `[[ED:field:value]]` for documented embedded data use.

Only use exact documented tags and syntax. Keep tags on their own line.

## Mapping policy

The bundled exporter maps common choice, scale, matrix, text, form, constant-sum, rank-order, and descriptive questions conservatively. It does not claim to implement arbitrary display/skip logic, quotas, scoring, JavaScript, carry-forward, Loop & Merge, sophisticated randomization, media interactions, hotspot/heat map, file upload, signature, video, or MaxDiff through undocumented tags.

Unsupported interactive questions become a descriptive programming marker plus a warning. This prevents silent loss while making manual work visible.

## Recodes and IDs

Use stable IDs and numeric recodes when analysis depends on coded values. Qualtrics may assign its own internal QIDs; inspect imported IDs and exported column names. Avoid duplicate IDs and duplicate choice recodes.

## Encoding and import

Use UTF-8 plain text, not UTF-16. Import into a test project. Inspect blocks, question types, layout, choices, recodes, and page breaks. Then program logic/validation/randomization in Qualtrics and test every path.

## Validation scope

`validate_qualtrics_txt.py` checks encoding, recognizable mode, unknown tags, duplicate IDs, missing text/choices/axes, and tag placement. It cannot guarantee current Qualtrics acceptance or semantic equivalence. The final authority is a successful test import and response export in the target Qualtrics environment.
