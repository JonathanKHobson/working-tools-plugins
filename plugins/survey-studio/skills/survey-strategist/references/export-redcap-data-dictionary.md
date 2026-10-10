# REDCap Data Dictionary

## Purpose

REDCap can import a CSV data dictionary describing fields, forms, choices/calculations, validation, identifiers, required status, branching logic, matrices, and annotations. Exact columns and supported syntax depend on the REDCap version/configuration.

## Mapping considerations

- canonical question ID → REDCap variable/field name, respecting naming constraints;
- block → form/instrument name;
- choice codes and labels → choices/calculations syntax;
- required, validation, min/max, identifier flag;
- branching logic in verified REDCap syntax;
- matrix group and ranking;
- notes, section headers, action tags, calculated fields, longitudinal events, repeating instruments.

The current skill does not generate a REDCap dictionary. Start from a data dictionary exported by the target REDCap project/version or current official template, map deliberately, and test import in a sandbox project.

## Risks

Do not guess action tags, overwrite a live project, expose PHI/PII in test data, or assume survey settings live entirely in the dictionary. Clinical/research governance may require a data management plan, IRB, HIPAA/security review, audit trails, and role-based access.

## QA

Import into a test project, review field names/types/codes/branching, test data entry and survey mode, export a test dataset, verify missing/checkbox conventions, and obtain the required project/governance approval before production.
