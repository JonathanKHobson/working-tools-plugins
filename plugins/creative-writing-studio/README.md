# Creative Toolkit

Turn an idea or existing draft into a finished story scene, a coherent story plan, or playable GM material while keeping canon and source boundaries visible. Bring the current draft or notes, the intended audience, and the output you want; the Studio selects the relevant craft route and produces that artifact.

Try “Revise this reveal for dread while preserving these canon facts,” “Make these campaign notes a reviewable Story Atlas,” or “Diagnose the stronger causal arc in these two endings.” Start with [creative-project-router](skills/creative-project-router/SKILL.md) for a broad request or [the task map](docs/use-case-map.md) for a named task. All first-party skill heads, methods, references, role contracts, templates and launchers are included in this package.

## Optional dependencies

The core writing, game preparation, rights and publication methods work from material you provide. Optional integrations require a recipient-installed runtime or provider skill:

- Creative-prose humanization: install the official `aihumanizer@openai-curated-remote` plugin through the native plugin manager; invoke `aihumanizer:creative-writing` when it appears in a refreshed task. Its independently maintained method is not bundled here. If unavailable, use this Studio's own story and prose methods without claiming the provider pass.
- [Creative Atlas](references/atlas-library.md): use the Activities Templates Atlas runtime and a recipient-owned approved catalog. `scripts/atlas_library_mcp.py` remains a fixed creative-domain compatibility launcher.
- [TTRPG Compass](references/ttrpg-compass.md): install its separately maintained backend and approved public data when a supported source/release is available. `scripts/ttrpg_compass_mcp.py` launches it; private campaigns are opt-in only.
- [Draw and Think](references/draw-think.md): install the separately maintained board backend when available; `scripts/draw_think_mcp.py` launches it with a recipient-owned data directory.

The three launchers are declared in [.mcp.json](.mcp.json) and require `python3` on PATH. Copy only the needed [example bindings](examples/runtime-bindings/) to `~/.config/studio-tools/`, replace placeholder paths with your own installed runtimes and data, and protect those files as local configuration. Do not copy the examples over an existing binding without review. The launchers report missing dependencies without downloading, changing, or exposing private data. A separately installed Activities Templates server may already expose the Creative Atlas view; use one registration for that view on a host.

TTRPG Compass and Draw and Think backend acquisition is currently a separate release boundary; this package ships its original workflow and launcher but cannot claim those servers are publicly installable until their owners publish a verified route. If an optional backend is absent, work from supplied material and say which capability was unavailable.

## Source and licensing

The stable package ID is `creative-writing-studio`; the display name is Creative Toolkit. The same distributable source lives in the canonical local owner and the public Working Tools package. Maintainers update the local source first, validate, and export identical distributable files. Native installation and GitHub publication are separate later steps.

First-party code is AGPL-3.0-only. First-party documentation, skills, methods and original creative templates are CC BY-SA 4.0. Novelist's MIT source and the GM Apprentice CC BY-SA 4.0 adaptation retain their original grants. See [licensing](LICENSING.md), [notices](THIRD_PARTY_NOTICES.md), and [source attributions](SOURCE-ATTRIBUTIONS.md). Atlas content, board state, campaign material and provider method bodies are not distributed here.

[Project map](docs/project-map.md) locates the entrypoints. [Source map](docs/source-to-target.md) records maintained method boundaries. Historical disabled standalone routes are compatibility paths; package activation is a separate native install step.
