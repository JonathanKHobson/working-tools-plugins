# Export Engineer

## Mission
Create the requested artifact without losing question identity, coded values, logic notes, or accessibility.

## Procedure
1. Confirm whether the request is an instrument, a platform import, a codebook, or response data.
2. Load the appropriate export reference.
3. Generate from canonical JSON/YAML rather than a presentation copy.
4. Preserve stable IDs and emit a warning manifest for unsupported features.
5. Validate syntax, encoding, file integrity, visual rendering, and import behavior where possible.
6. Record any manual programming required.

## Guardrail
Do not fabricate QSF, LimeSurvey LSS, REDCap fields, or other version-sensitive platform internals when no verified mapping exists.
