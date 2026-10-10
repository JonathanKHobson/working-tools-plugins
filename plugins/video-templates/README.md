# Video Templates

Current edition **0.1.3** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Reusable video discovery and editable storyboarding, with one skill and the existing `video-style-library` MCP interface. The public catalog contains 30 families, 38 exact examples and seven distinct pinned staged methods. Catalog selection preserves hashes, rights summaries, review limits and source availability. Video Production Studio retains production and render QA.

Start with [onboarding](docs/onboarding.md), [the discovery skill](skills/video-templates/SKILL.md), [source provenance](docs/source-provenance.json) and [rights/dependencies](docs/rights.md). The [project map](docs/project-map.md) identifies the maintained boundaries.

The public edition includes the complete chooser, catalog adapter, eleven MCP tools, two app resources, revisioned storyboard store, media validation and seven pinned MIT animation methods. The 30-family/38-example catalog is a factual metadata projection: identities, technical hashes, public links, availability and source-reported rights summaries. Creative prompts, film recipes, fonts, music, films and reference bundle bodies are excluded. The originating public links keep those materials at their existing owners. An explicit user-supplied catalog can provide richer material under that user's rights.

Install from the [Working Tools guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md). Python 3.10+ and the dependencies in `requirements.txt` are required. Root `plugin.json`/`mcp.json` supply the portable local stdio definition; `.codex-plugin`, `.claude-plugin` and `.mcp.json` supply host compatibility metadata. Set `VIDEO_TEMPLATES_PYTHON` to your MCP-equipped interpreter when needed. Private state and host bindings stay outside the package.

Run `python3 scripts/validate.py`, then use the selected MCP-equipped interpreter for `tests/test_stdio.py`. The test relocates the complete package and uses a fresh private fixture: it lists real tools/resources, validates exact method/example hashes, creates and patches a storyboard, checks idempotent retry and revision conflict, reads sketch media and prepares the separate drawing handoff. A missing provider is not a missing storyboard backend. Native host widget interaction and film reproduction remain separate receiving-host checks.

## Source and collection continuity

The distributable runtime, full operative methods and eligible maintenance code are shared by canonical source and this package. Held collection bodies remain in the source owner's private installation with exact per-file export exclusions and prechange archives. Recipient installations need their own authorized collection where described below; synthetic fixtures prove the interface and do not replace a maintained private collection.

The existing external Video bindings object supports `catalog` and `preview_root`, alongside interpreter, private storyboard database and chooser bindings. Explicit `VIDEO_LIBRARY_CATALOG` and `VIDEO_LIBRARY_PREVIEW_ROOT` win. This keeps original held recipe narratives and previews selectable without replacing private data with public examples. The public 30-family/38-example metadata and seven full MIT animation methods remain; original creative recipe bodies and previews need an authorized external collection.
