# JSON Export

## Best for

Canonical machine-readable definitions, API integration, deterministic generation, JSON Schema validation, version control, and lossless interchange for the skill’s represented model.

Generate:

```bash
python scripts/export_survey.py survey.yaml survey.json --format json
```

Validate against `assets/survey.schema.json` through the loader/scripts.

## Rules

- UTF-8 and RFC 8259-compatible JSON;
- no comments or trailing commas;
- stable IDs and explicit display labels vs machine values;
- ISO-style timestamps/dates only when semantics are documented;
- preserve numeric values as numbers, not locale-formatted strings;
- define extension namespaces or `platform_notes` rather than inventing ambiguous top-level fields;
- version the schema and instrument.

## QA

Parse with an independent JSON parser, schema-validate, compare counts/IDs, test round-trip to YAML and generated outputs, and verify no NaN/Infinity or duplicate keys. Canonicalization/hash rules must be specified separately if signatures or exact byte comparison matter.
