# Writing Templates

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

[MIT](LICENSE) covers the authorized first-party public runtime, chooser and authored test code. External collection rights remain separate. No private corpus, personal voice samples, brand artwork, provider assets, credentials or host configuration is included. See [third-party notices](THIRD_PARTY_NOTICES.md) and exact source/output hashes in `PROVENANCE.json`. Report package version, host and a synthetic reproduction through the Working Tools repository; support is best effort.
