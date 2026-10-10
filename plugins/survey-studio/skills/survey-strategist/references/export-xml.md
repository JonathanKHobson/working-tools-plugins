# XML Export

## Best for

Integrations that require XML, validation against an agreed XSD, archival interchange, or formal survey metadata standards such as DDI when that ecosystem is required.

Generate the skill’s generic XML projection:

```bash
python scripts/export_survey.py survey.yaml survey.xml --format xml
```

## Design

Use UTF-8, one unambiguous root element, explicit IDs/attributes, escaped text, namespaces when extending, and an accompanying schema or mapping for external integrations. Preserve code/label distinction and do not encode essential order through unordered structures.

Generic XML is not automatically DDI, LimeSurvey LSS, or another platform’s import format. Standards require their own schema/version and mappings.

## Security

Disable external entity resolution and DTD fetching when parsing untrusted XML. Protect against entity expansion and oversized documents.

## QA

Parse with an independent library, validate against the required XSD when available, verify namespaces/encoding, compare counts/IDs, and test the receiving system. Pretty printing must not alter mixed-content meaning.
