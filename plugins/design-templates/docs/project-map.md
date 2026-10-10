# Public runtime project map

Design Templates owns the complete first-party source-integrity chooser and workflow. Private templates and reference assets are excluded.

- plugin.json/mcp.json supply portable launch metadata; native manifests expose the same route.
- scripts/design_library_mcp.py selects an explicit MCP interpreter before server startup.
- runtime/design-library/ owns catalog validation, source fingerprinting, guidance provenance, handoff, real MCP tools/resources, domain adapter and private feedback helper.
- runtime/library-chooser/ retains the maintained shared UI source. scripts/sync_library_chooser.py preserves its existing maintenance method.
- scripts/template_catalog.py reads the explicitly supplied external full-format inventory/recipes; scripts/check_template_tokens.py owns bounded CSS token checks.
- skills/design-templates/ retains the operative adaptation and authoring-acceptance workflow.
- scripts/create_sample_collection.py creates a clearly labeled external source-integrity fixture; it contains no private collection material.
- Default runtime and full-format catalogs are empty; three original conditional adaptation recipes remain in templates/adaptation-recipes.json. External data binding and rights are documented in docs/setup.md and docs/rights.md.
- tests retain source/guidance tamper, symlink, path, serialization and token checks; the public stdio test executes a supplied fixture.

Run the documented unit suites and public stdio test with the selected MCP environment. Generated evidence and private state stay outside package source.
