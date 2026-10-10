# SurveyJS JSON

## Purpose

SurveyJS uses a JSON survey model to render forms in web applications. It supports pages/elements, choices, validation, conditional visibility, calculated values, localization, and many component types, but the exact schema depends on the SurveyJS version and licensed components.

## Mapping workflow

1. Pin the SurveyJS library and creator versions.
2. Map canonical blocks to pages/panels and question types to supported elements.
3. Preserve canonical IDs in `name` or a documented metadata field.
4. Map display logic to verified SurveyJS expressions.
5. Map values/labels, required rules, validators, locale text, and completion behavior.
6. Record unsupported properties in a warning manifest.
7. Validate with the target SurveyJS runtime/Creator and submit test data.

The current skill does not emit SurveyJS JSON automatically. Do not treat generic canonical JSON as drop-in SurveyJS JSON.

## Security and privacy

Rendering is not data storage. Implement an approved backend, server-side validation, authentication/authorization, CSRF/rate limiting, encryption, retention, consent, and safe handling of uploads/HTML.

## QA

Pin schema/version, load without console errors, inspect all pages and conditions, keyboard/screen-reader/mobile test, verify values in completion payload, test localization, and compare to the canonical codebook.
