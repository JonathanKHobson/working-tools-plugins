# Design Templates

Current edition **0.1.6** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Complete first-party Design Library runtime for explicitly supplied editable sources: source-integrity search, human chooser, hash-bound handoff, token checks and inventory/recipe tools. The authorized public edition includes all original runtime code and operative workflow; the private 112-template collection, preview assets, font/artwork and provider materials are excluded.

Install through the [Working Tools guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md). Python 3.10+ and requirements.txt are needed for local stdio. Set DESIGN_LIBRARY_PYTHON to that environment when the stock host python3 lacks MCP. The stdlib launcher selects the interpreter before the server imports the SDK.

For a safe first use, run `scripts/create_sample_collection.py --output <empty-external-folder>` with the selected environment. Set DESIGN_LIBRARY_CATALOG and DESIGN_TEMPLATES_DATA_ROOT to its emitted paths. Ask to search the synthetic example and prepare its verified handoff. The fixture is clearly labeled source-integrity evidence, not an equivalent Studio template. Replace those bindings only with your own authorized collection, matching source hashes and provenance. The package's default catalog is empty; installation grants no private collection access.

[The discovery skill](skills/design-templates/SKILL.md) retains source-fidelity adaptation, source tokens, selected guidance, Office-provider handoff and template-authoring acceptance. [Setup](docs/setup.md) documents external data. [Project map](docs/project-map.md) locates the complete modules. [Rights](docs/rights.md) distinguishes code from supplied data.

Run the selected interpreter with `-B -m unittest discover -s runtime/design-library/tests -v`, then `-B -m unittest discover -s tests -v`. `tests/test_public_stdio.py` exercises the stock bootstrap, actual search, source/guidance integrity handoff and real gallery resource against an external authored fixture. A selected source is a handoff, not a deployed site or completed Office export.

## Source and collection continuity

The distributable runtime, full operative methods and eligible maintenance code are shared by canonical source and this package. Held collection bodies remain in the source owner's private installation with exact per-file export exclusions and prechange archives. Recipient installations need their own authorized collection where described below; synthetic fixtures prove the interface and do not replace a maintained private collection.

The existing external `~/.config/studio-tools/design-library.json` may retain `interpreter` and add `collections.design-templates` with `catalog`, `data_root`, `full_catalog` and `asset_manifest`. `scripts/template_catalog.py` then searches and verifies that complete source inventory. Explicit `DESIGN_TEMPLATES_DATA_ROOT` chooses its own collection and suppresses private default pins; explicit catalog/manifest environment selectors win. The public empty collection excludes the held 112-template body, fonts and previews; the complete chooser and three adaptation recipes remain.
