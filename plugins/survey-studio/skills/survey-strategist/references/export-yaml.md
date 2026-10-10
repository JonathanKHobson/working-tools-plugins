# YAML Export

## Best for

Human-authored canonical instruments, readable diffs, reusable templates, and structured configuration with JSON-compatible data.

Generate:

```bash
python scripts/export_survey.py survey.json survey.yaml --format yaml
```

## Rules

Use YAML 1.2-compatible syntax, UTF-8, spaces rather than tabs, and explicit quoting where implicit typing could change values (for example `yes`, dates, or numeric-looking IDs). Avoid custom tags, anchors/aliases, merge keys, and executable constructors unless the target explicitly supports and safely handles them.

Treat YAML as untrusted input. Use safe loaders. Validate the resulting object against `assets/survey.schema.json`.

## QA

Load with a safe YAML parser, schema-validate, round-trip to JSON, compare IDs/types/values, and inspect multiline text. Different YAML implementations vary; keep the subset conservative.
