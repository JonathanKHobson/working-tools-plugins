# LimeSurvey LSS

## Purpose

LSS is a LimeSurvey survey-structure export, generally XML containing survey groups, questions, answers, language text, and settings. Its schema and supported properties can vary by LimeSurvey version/plugins.

## Policy

Do not generate or edit LSS from memory. Export a minimal survey from the exact target LimeSurvey version, use it as a verified structural reference, consult current documentation, and validate in a disposable instance.

## Mapping workflow

1. Pin LimeSurvey version, languages, and plugins.
2. Export a minimal LSS from that environment.
3. Map canonical IDs/types/choices/groups into the verified schema.
4. Preserve language and relevance-equation behavior.
5. Record unsupported settings and manual steps.
6. Import into a test instance and submit/export test responses.

## QA

Validate XML, import without warnings, inspect question themes/types, relevance equations, quotas, assessments, tokens/anonymity, language text, permissions, and response export. Do not overwrite a production survey without a backup and rollback plan.
