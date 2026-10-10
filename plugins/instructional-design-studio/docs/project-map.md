# Project map

## Ownership

This plugin is independent of job-application-compass. Portable source: this independently versioned package in Working Tools. Native marketplaces and installed caches are separate. No source corpus is copied here and no external service is a live dependency for ordinary skill use.

## Layout

- `.codex-plugin/plugin.json`: plugin identity, discovery, and starter prompts.
- `skills/*/SKILL.md`: twelve separate, narrowly described capabilities, including the complete first-party `learning-experience-designer` method. `docs/learning-experience-designer-source.json` records its source and output hashes.
- `skills/*/agents/openai.yaml`: display names and invocation prompts.
- `skills/*/references/`: conditional guidance, method/source notes, and worked examples.
- `skills/*/assets/`: examples/templates intended for adaptation into deliverables.
- `skills/*/scripts/`: read-only JSON checkers using Python's standard library.
- `tests/`: local helper regression checks; no network or learner data.
- `docs/verification.md`: package checks and observed behavioral validation, with limits.
- `README.md`: human-facing catalog and usage.

## Reading order

Start with the narrow skill for a clear requested output; use the instructional-design router for broad or mixed work. README is a human catalog, not a mandatory runtime read. Load references only for the decision at hand. Personal style uses the grounding reference; research rationale uses the relevant evidence section. The neighboring plugin is optional, not an import dependency.

`instructional-design/references/addie-decisions.md` owns lifecycle decisions and the compact evidence, traceability, and dependency records. Needs-analysis, evaluation, lesson, and production references own their specialist detail. `research-intake-2026-09.md` records the two supplied syntheses and selective source checks; it is for provenance review, not routine loading. Maintenance challenge cases live in `docs/behavior-cases.json`, outside the runtime skill path.

## Changes and validation

Edit the owning skill for behavior changes, its reference for detailed procedures, and its asset for sample output. Keep shared guidance within this plugin and reference it relatively. Do not make symlinks to external corpora. Validate each changed SKILL.md using skill-creator, then validate the plugin manifest with plugin-creator. Execute a changed helper against valid and invalid examples. Recheck realistic task behavior after substantive instruction changes.

Generated caches, ZIP files, and temporary evaluation outputs stay outside the plugin source. Existing global skills remain unchanged. No runtime hooks, learner tracking, account connections, or additional MCPs are configured.

The AI Workshop Studio v3 planning path is a bounded extension of `skills/instructional-design`. Its conditional reference, portable `studio-v3-1` contract, provenance record, and checker live together under that skill. The app-owned contract remains authoritative; the portable copy supports offline skill use and the checker detects drift when both paths are available. Project-specific evaluation fixtures and the implementation receipt remain in the Studio planning-foundation worktree, not in this reusable plugin.

`ai-literacy-education/references/course-adaptation.md` holds conditional guidance for partial-course evidence, cross-product adaptations, simulated perspectives, and changed-input reuse. Course-specific workstreams and live product facts stay with the owning course task.

`course-production-handoff/references/course-media-integration.md` owns script/resource reconciliation, clip-to-lesson mapping, and learner revision checks. Video Production Workflow owns the recorded media; Writing Quality Studio owns an optional spoken-voice pass.

## Assessment and activity extension

`assessment-rubric-design` owns blueprint/item/assignment/scoring guidance, source review, a fictional JSON authoring example and `scripts/check_assessment.py`. It does not own delivery platforms or Survey Studio's instrument engine. `lesson-experience-design` owns `assets/activity-library.json` and `scripts/search_activities.py`: 31 complete original adaptations with source identities. The helper selects an explicit `--library`, then an optional recipient-owned studio-tools binding, then the bundled adaptations. A broken binding fails visibly. Search a few matches, then author concrete materials. Neither helper fetches source URLs or writes to the vault. `learning-evaluation` owns score interpretation and pilot/transfer decisions.

Safe checks from this root: `python3 -m unittest discover -s tests -v`; `python3 skills/assessment-rubric-design/scripts/check_assessment.py skills/assessment-rubric-design/assets/assessment-template.json`; `python3 skills/lesson-experience-design/scripts/search_activities.py --query retrieval --limit 3`. Helpers require Python 3.9+ standard library; use an already available bundled runtime if system Python is unavailable. Draft warnings are expected. Source audit: `docs/assessment-security-review.md`. Activity sources remain personal-reference-only; a passing checker is not learning validation.

`lesson-experience-design/references/technical-learning-resource-selection.md` owns the conditional tutorial/catalog viability check: selected destination, rights, setup, learner task and capability evidence. It imports no curriculum or learning platform.

- `references/atlas-library.md`: scoped instructional Atlas retrieval and private human library. The portable edition includes the fixed-domain compatibility launcher at `scripts/atlas_library_mcp.py`, with recipient-owned `--binding` or the current user’s standard studio-tools path. No MCP service, automatic declaration or corpus is packaged.

`learning-content-storyboarding/references/writing-voices.md` is the conditional bridge to the canonical writing owner; learning goals, practice, feedback, assessment and source accuracy stay with this plugin.

## Public edition

All operative skill heads and their complete generic supporting procedures are preserved. Empty private MCP declarations are excluded; the portable fixed-domain compatibility launcher is included; optional Atlas/source retrieval uses the current host's separately configured capability. PROVENANCE.json records all input/output hashes and exclusions. Private history locators and unknown-rights archive/source summaries are excluded. See SOURCE-ATTRIBUTIONS.md and docs/release-validation.md.

Standalone method owners in 0.2.0: `skills/learning-experience-designer/`. Preserve full original procedures and their exact source/recipient-output hashes in PROVENANCE.json. Populated recipient inputs belong outside installation state.
