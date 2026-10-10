# Brand Templates

Current edition **0.1.2** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Complete original first-party brand kit selection, source-closure verification and handoff runtime by Kyle Hobson. This public edition includes the actual MCP app and chooser, with three tools and one resource.

The original 104 fictional reusable kits are included with complete guides, editable guide source, source-verified previews, outlined logo artwork, asset manifests and exact open-font notices. The separately added Fresh Curiosity A2 kit is excluded because its character/raster asset provenance needs a separate release review. You may use the included collection, explicitly bind another authorized collection, or create the clearly labelled synthetic contract fixture below. The fixture verifies software behavior; it is not a substitute collection or a demonstration of brand quality or writing style.

## Setup and first task

Use Python 3.10+ in a dedicated environment. Startup never installs dependencies. Stock Python can run the stdlib launcher, which selects the configured interpreter before importing MCP:

```sh
python3.12 -m venv /your/external/brand-templates-venv
/your/external/brand-templates-venv/bin/python -m pip install -r requirements.txt
export BRAND_TEMPLATES_PYTHON=/your/external/brand-templates-venv/bin/python
python3 scripts/create_sample_collection.py --output /your/external/brand-templates-fixture
export BRAND_TEMPLATES_DATA_ROOT=/your/external/brand-templates-fixture
```

Register through the host's plugin manager using this package's portable `plugin.json` and `mcp.json`, Codex `.codex-plugin/plugin.json` and `.mcp.json`, or Claude `.claude-plugin/plugin.json` and `.mcp.claude.json`. Keep interpreter/data variables in host configuration outside this package, and expose one effective `brand-library` registration per host. Start a fresh host session after installation.

Ask the assistant to search Brand Templates for synthetic, then prepare the fixture-neutral handoff using only a fictional brief. Search and handoff do not open a widget; browse deliberately presents the chooser. A handoff is prepared text, not a saved artifact, sent message or publication.

Export the exact resource for standalone inspection:

```sh
python3 scripts/brand_library_mcp.py --export-html /your/external/brand-templates-gallery.html
```

Standalone Use provides a copyable fallback and does not claim MCP verification. Native host rendering and provider execution remain separate checks. Read [the collection contract](docs/collection-contract.md) and [project map](docs/project-map.md).

## Verification

Guide-source regeneration additionally needs the optional `requirements-render.txt` dependencies and the selected kit's notices. Existing guides and raster previews do not require those packages.

Run `"${BRAND_TEMPLATES_PYTHON}" -B -m unittest discover -s tests -p 'test_public_stdio.py' -v` with the selected MCP interpreter. Tests relocate the package, create external data, start the actual stdio server through the stock-interpreter launcher, exercise every core tool and resource, reject source mutations/traversal, and preserve source data. Rendering/adapting a real kit requires its separately supplied asset and font licenses plus an appropriate output provider.

## Rights and support

[AGPL-3.0-only](LICENSE) covers first-party code; [CC BY-SA 4.0](legal/LICENSE-DOCS-CC-BY-SA-4.0.md) covers original documentation, methods and eligible templates. External collection rights remain separate. The included fictional original brand artwork is covered by the current author authorization; exact bundled font files retain SIL OFL rights. No private personal corpus, provider assets, credentials or host configuration is included. See [third-party notices](THIRD_PARTY_NOTICES.md) and exact source/output hashes in `PROVENANCE.json`. Report package version, host and a synthetic reproduction through the Working Tools repository; support is best effort.
