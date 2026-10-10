# Writing Templates

Current edition **0.1.4** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Complete original first-party writing resource selection, base/module routing, source verification, handoff and offline draft QA runtime by Kyle Hobson. This public edition includes the actual MCP app and chooser, with three core tools and one resource, plus two optional private feedback tools.

The original 53-resource writing collection, style guides, historical readings, demonstrations, axis profiles, artwork and prose companions is excluded. The default chooser is empty. Supply a collection you are authorized to use, or create the clearly labelled synthetic contract fixture below. The fixture verifies software behavior; it is not a substitute collection or a demonstration of brand quality or writing style.

## Setup and first task

Use Python 3.10+ in a dedicated environment. Startup never installs dependencies. Stock Python can run the stdlib launcher, which selects the configured interpreter before importing MCP:

```sh
python3.12 -m venv /your/external/writing-templates-venv
/your/external/writing-templates-venv/bin/python -m pip install -r requirements.txt
export WRITING_TEMPLATES_PYTHON=/your/external/writing-templates-venv/bin/python
python3 scripts/create_sample_collection.py --output /your/external/writing-templates-fixture
export WRITING_TEMPLATES_DATA_ROOT=/your/external/writing-templates-fixture
```

Register through the host's plugin manager using this package's portable `plugin.json` and `mcp.json`, Codex `.codex-plugin/plugin.json` and `.mcp.json`, or Claude `.claude-plugin/plugin.json` and `.mcp.claude.json`. Keep interpreter/data variables in host configuration outside this package, and expose one effective `writing-voice-library` registration per host. Start a fresh host session after installation.

Ask the assistant to search Writing Templates for synthetic, then prepare P28 with a fictional brief and inspect its actual V01 + P28 route. Search and handoff do not open a widget; browse deliberately presents the chooser. A handoff is prepared text, not a saved artifact, sent message or publication.

Export the exact resource for standalone inspection:

```sh
python3 scripts/writing_voice_library_mcp.py --export-html /your/external/writing-templates-gallery.html
```

Standalone Use provides a copyable fallback and does not claim MCP verification. Native host rendering and provider execution remain separate checks. Read [the collection contract](docs/collection-contract.md) and [project map](docs/project-map.md).

## Verification

Run `"${WRITING_TEMPLATES_PYTHON}" -B -m unittest discover -s tests -p 'test_public_stdio.py' -v` with the selected MCP interpreter. Tests relocate the package, create external data, start the actual stdio server through the stock-interpreter launcher, exercise every core tool and resource, reject source mutations/traversal, and preserve source data. The actual offline writing engine also requires Node 20+; run `node --test tests/test_voice_validation.cjs`. Its metrics describe prose, and a successful exit never proves style quality or factual correctness.

## Rights and support

[AGPL-3.0-only](LICENSE) covers first-party code; [CC BY-SA 4.0](legal/LICENSE-DOCS-CC-BY-SA-4.0.md) covers original documentation, methods and eligible templates. External collection rights remain separate. No private corpus, personal voice samples, brand artwork, provider assets, credentials or host configuration is included. See [third-party notices](THIRD_PARTY_NOTICES.md) and exact source/output hashes in `PROVENANCE.json`. Report package version, host and a synthetic reproduction through the Working Tools repository; support is best effort.

## Source and collection continuity

The distributable runtime, full operative methods and eligible maintenance code are shared by canonical source and this package. Held collection bodies remain in the source owner's private installation with exact per-file export exclusions and prechange archives. Recipient installations need their own authorized collection where described below; synthetic fixtures prove the interface and do not replace a maintained private collection.

The launcher retains the shared Design interpreter binding. Optional `collections.writing-templates` selects `data_root`, `approved_sources` and `public_base`; explicit `WRITING_TEMPLATES_*` values win. An explicit data root suppresses private default pins. The source owner keeps all 53 guides, examples, historical readings, axis pages and QA profiles at their original collection path with privately selected hash pins. The public engine and maintenance builders remain complete; collection-dependent tests/builders require recipient-owned source data. The empty public collection cannot supply those 53 resources. Original Writing Voice Lab inventory and approval pins stay private.

The synthetic fixture builder uses an explicit eleven-file engine/support allowlist, including the pinned MIT parser and license, and creates only four authored profiles. It cannot inherit unrelated source-owner collection profiles, prose or maintenance scripts.
