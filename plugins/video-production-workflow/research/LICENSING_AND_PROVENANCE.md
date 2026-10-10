# Licensing, Rights, and Provenance

## Source usage classes

- **runtime-dependency:** packaged or installed under a compatible license.
- **optional-integration:** supported but not required; remains separately licensed.
- **invoke-external-tool:** call the installed binary; do not copy its source into this MIT plugin.
- **adapt-ideas-with-attribution:** permissively licensed workflow ideas may be reimplemented; preserve notices when code is copied.
- **research-only-no-copy:** learn from public behavior and documentation, but do not redistribute unlicensed text/code.
- **delivery-reference-reverify:** platform facts are used only with a current review date.

## Asset provenance record

Each source or generated asset should include:

```json
{
  "id": "stable-id",
  "path": "source/file.mov",
  "sha256": "...",
  "creator": "person/provider/model",
  "source_url": "...",
  "acquired_at": "ISO-8601",
  "license_or_permission": "...",
  "redistribution_allowed": false,
  "model_and_version": "...",
  "prompt_or_generation_record": "...",
  "parent_assets": ["..."],
  "notes": "..."
}
```

## Critical cautions

- Possessing a file does not prove editing, publication, likeness, music, stock, or model rights.
- A font file’s presence does not grant redistribution or commercial use.
- Open-source software license and generated media license are different questions.
- GPL/AGPL tools can often be used as separate applications, but copying/linking/distribution decisions require care.
- Source-available is not synonymous with open source; verify Remotion’s current terms for the organization and use.
- Platform downloads should require user rights and applicable site permission.
- AI-generated media may still raise provider terms, training-data, trademark, likeness, and jurisdictional issues.

This plugin is not legal advice. It makes uncertainty visible and prevents silent rights assumptions.
