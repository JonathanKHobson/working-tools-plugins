# Project map

## Ownership

This plugin is independent of job-application-compass. Portable source: this independently versioned package in Working Tools. Native marketplaces and installed caches are separate. No source corpus is copied here and no external service is a live dependency for ordinary skill use.

## Layout

- `.codex-plugin/plugin.json`: plugin identity, discovery, and starter prompts.
- `skills/*/SKILL.md`: separate, narrowly described capabilities.
- `skills/*/agents/openai.yaml`: display names and invocation prompts.
- `skills/*/references/`: conditional guidance, method/source notes, and worked examples.
- `skills/*/assets/`: examples/templates intended for adaptation into deliverables.
- `skills/*/scripts/`: read-only JSON checkers using Python's standard library.
- `docs/verification.md`: package checks and observed behavioral validation, with limits.
- `README.md`: human-facing catalog and usage.

## Reading order

Read README, then the narrow skill for the requested output. Load only its relevant references. For personal style or source claims, read the grounding reference. For research rationale, read the evidence reference. The neighboring plugin is optional, not an import dependency.

For collaborative boards, `workshop-design/references/agenda-format.md` owns the active-task/reveal run sheet and review lifecycle; `workshop-decision-making/references/decision-patterns.md` owns the evidence-to-options-to-decision-to-accepted-action chain. Figma Studio retains actual-editor operations and capability testing. Source rationale and limitations live in the existing facilitation-evidence reference.

## Changes and validation

Edit the owning skill for behavior changes, its reference for detailed procedures, and its asset for sample output. Keep shared guidance within this plugin and reference it relatively. Do not make symlinks to external corpora. Validate each changed SKILL.md using skill-creator, then validate the plugin manifest with plugin-creator. Execute a changed helper against valid and invalid examples. Recheck realistic task behavior after substantive instruction changes.

Generated caches, ZIP files, and temporary evaluation outputs stay outside the plugin source. Existing global skills remain unchanged. No runtime hooks, learner tracking, or account connections are configured. The optional private Atlas MCP below supports activity lookup.


- `references/atlas-library.md`: scoped facilitation Atlas retrieval and private human library. The public method edition includes no launcher or MCP declaration; separately configured receiving-host retrieval is optional, and no corpus is packaged.

## Public edition

All operative skill heads and their complete generic supporting procedures are preserved. Empty private MCP declarations and the machine compatibility launcher are excluded; optional Atlas/source retrieval uses the current host's separately configured capability. PROVENANCE.json records all input/output hashes and exclusions. Private history locators and unknown-rights archive/source summaries are excluded. See SOURCE-ATTRIBUTIONS.md and docs/release-validation.md.
