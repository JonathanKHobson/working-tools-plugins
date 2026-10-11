# Creative Toolkit

Portable MCP discovery is supported through root [`mcp.json`](mcp.json) for the existing optional launchers. Their server identities, runtime bindings and compatibility declarations are preserved; backend availability remains a separate check.

Turn an idea or existing draft into a finished story scene, a coherent story plan, or playable GM material while keeping canon and source boundaries visible. Bring the current draft or notes, the intended audience, and the output you want; the Studio selects the relevant craft route and produces that artifact.

Try “Revise this reveal for dread while preserving these canon facts,” “Make these campaign notes a reviewable Story Atlas,” or “Diagnose the stronger causal arc in these two endings.” Start with [creative-project-router](skills/creative-project-router/SKILL.md) for a broad request or [the task map](docs/use-case-map.md) for a named task. All first-party skill heads, methods, references, role contracts, templates and launchers are included in this package.

## Optional dependencies

The core writing, game preparation, rights and publication methods work from material you provide. Optional integrations require a recipient-installed runtime or external service:

- [Creative Atlas](references/atlas-library.md): use the Activities Templates Atlas runtime and a recipient-owned approved catalog. `scripts/atlas_library_mcp.py` remains a fixed creative-domain compatibility launcher.
- [TTRPG Compass](references/ttrpg-compass.md): install its separately maintained backend and approved public data when a supported source/release is available. `scripts/ttrpg_compass_mcp.py` launches it; private campaigns are opt-in only.
- [Draw and Think](references/draw-think.md): install the separately maintained board backend when available; `scripts/draw_think_mcp.py` launches it with a recipient-owned data directory.

The three launchers are declared in portable [mcp.json](mcp.json), with [.mcp.json](.mcp.json) retained for compatibility and require `python3` on PATH. Copy only the needed [example bindings](examples/runtime-bindings/) to `~/.config/studio-tools/`, replace placeholder paths with your own installed runtimes and data, and protect those files as local configuration. Do not copy the examples over an existing binding without review. The launchers report missing dependencies without downloading, changing, or exposing private data. A separately installed Activities Templates server may already expose the Creative Atlas view; use one registration for that view on a host.

TTRPG Compass and Draw and Think backend acquisition is currently a separate release boundary; this package ships its original workflow and launcher but cannot claim those servers are publicly installable until their owners publish a verified route. If an optional backend is absent, work from supplied material and say which capability was unavailable.


## Host compatibility

| Capability | Codex | Claude Code |
| --- | --- | --- |
| First-party skills and packaged methods | Native installation and synthetic first-use verified | Native installation and file parity verified; first-use behavior still needs a host test |
| Still-image generation | Use the host’s available `imagegen` capability and verify its output | Use a separately available, authorized image provider; the Codex `imagegen` route is not supplied by this package |
| Optional MCP launchers | Portable `mcp.json` uses `${PLUGIN_ROOT}` paths and working directory | The Claude manifest uses `${CLAUDE_PLUGIN_ROOT}` paths; backend execution remains a separate acceptance check |

## Source and licensing

The stable package ID is `creative-writing-studio`; the display name is Creative Toolkit. The same distributable source lives in the canonical local owner and the public Working Tools package. Maintainers update the local source first, validate, and export identical distributable files. Native installation and GitHub publication are separate later steps.

First-party code is AGPL-3.0-only. First-party documentation, skills, methods and original creative templates are CC BY-SA 4.0. Novelist's MIT source and the GM Apprentice CC BY-SA 4.0 adaptation retain their original grants. See [licensing](LICENSING.md), [notices](THIRD_PARTY_NOTICES.md), and [source attributions](SOURCE-ATTRIBUTIONS.md). Atlas content, board state, campaign material and provider method bodies are not distributed here.

[Project map](docs/project-map.md) locates the entrypoints. [Source map](docs/source-to-target.md) records maintained method boundaries. Historical disabled standalone routes are compatibility paths; package activation is a separate native install step.
