# Game Creation Studio

Current edition **0.3.2** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Design a playable game or prepare and facilitate a tabletop session. Turn a game idea into a playable, testable slice. Start with the player's repeated choice, decide what must exist for one complete run, build that slice in the game's owning project, and test it with players. The package also preserves the full third-party Game Development Studio 1.0.2 methods for assets, package vendoring, render diagnosis, and performance work.

Try: "Find the core loop in this game idea," "Scope this to a weekend prototype," or "Use this capture to diagnose the renderer." Useful input is a concept or project, target platform, audience, current build, and one decision to make. The result is a game-specific design, implementation handoff, or evidence-backed diagnosis, according to the request.

## Choose a skill

| Request | Skill |
| --- | --- |
| Cross-discipline help or "what can this do?" | [game-creation-studio](skills/game-creation-studio/SKILL.md) |
| Player fantasy, verbs, loop, stakes, feedback | [game-core-loop](skills/game-core-loop/SKILL.md) |
| Small playable slice, milestone, cut list | [game-prototype-scope](skills/game-prototype-scope/SKILL.md) |
| Rules, progression, balance, save/state | [gameplay-systems](skills/gameplay-systems/SKILL.md) |
| HUD, controls, onboarding, accessibility | [game-ui-accessibility](skills/game-ui-accessibility/SKILL.md) |
| Playtest, triage, release evidence | [game-playtest-release](skills/game-playtest-release/SKILL.md) |
| Produce and package 3D, texture, audio assets | [game-asset-production](skills/game-asset-production/SKILL.md) |
| Check license/hash and admit packages | [game-asset-vendoring](skills/game-asset-vendoring/SKILL.md) |
| Capture and locate render defects | [game-visual-debugging](skills/game-visual-debugging/SKILL.md) |
| Compare runs and optimize one metric | [game-performance-optimization](skills/game-performance-optimization/SKILL.md) |


For board/card games, use [Board Game Design](skills/board-game-design/SKILL.md); for cross-domain diagnosis, use [Game Designer](skills/game-designer/SKILL.md) and its full references. For campaigns and GM work, start with [TTRPG Router](skills/ttrpg-router/SKILL.md) or [GM Roleplay Router](skills/gm-roleplay-router/SKILL.md), then select the smallest included live, pacing, NPC, player, rules, safety, public-table, roleplay or debrief method. All fifteen added workflows and their complete support files are listed in [recipient bindings and routes](docs/standalone-workflow-bindings.md). The optional style layer is removable; actual rulebooks, campaign canon and table preferences remain recipient inputs.

For browser implementation, route to the **separately installed OpenAI Game Studio** skill named in [the routing table](docs/routes.json). This package does not copy or replace its code, scripts, assets, or starter projects. Engine-specific game work may need the owning engine's own tools.

## Setup and capability boundary

The skill methods are readable without a service. The preserved third-party asset/capture/performance commands require a separately installed `game-dev` CLI, version 1.0.2 or newer for provider operations, plus the target project and any applicable local tools. This package contains **no CLI binary, MCP server, hook, provider account, credential, or background service**. Check `command -v game-dev`, `game-dev --version`, `game-dev capabilities --json`, and `game-dev doctor --json` only when the command is actually needed. A missing executable blocks those commands, not design and playtest work.

Provider generation needs a user-controlled account and credential already configured outside the conversation. Keep each paid request, project execution, GPU capture, hardware measurement, and local write scoped to its resolved invocation. Review current provider terms and license for actual assets. The preserved [upstream README](vendor/game-development-studio-1.0.2/README.md), [privacy](vendor/game-development-studio-1.0.2/PRIVACY.md), [terms](vendor/game-development-studio-1.0.2/TERMS.md), [security](vendor/game-development-studio-1.0.2/SECURITY.md), and [support](vendor/game-development-studio-1.0.2/SUPPORT.md) describe the original package, not a service operated by Game Creation Studio.

## Provenance and review state

The complete Game Development Studio 1.0.2 source snapshot is retained under [vendor](vendor/game-development-studio-1.0.2/), with its [MIT license](vendor/game-development-studio-1.0.2/LICENSE). Four active technical skills are byte-identical copies of its focused methods. The former umbrella method is preserved in the snapshot and integrated into the new router. Original design skills are new material. Original Game Creation Studio contributions by Jonathan Kyle Hobson are released under the scoped first-party licenses described in LICENSING.md. Benjamin Michael Haire / Ben Haire retains copyright in the complete MIT vendor source and byte-identical technical skill copies. See [third-party notices](THIRD_PARTY_NOTICES.md), [coverage](provenance/coverage.json), and [project map](docs/project-map.md).

Native installation and discovery are separate host checks. Static checks do not establish live skill discovery, CLI availability, provider readiness, visual quality, or a shipped game.

## Run a bounded check

Read [installation](docs/installation.md), then run `python3 -B tests/validate.py` from this root. The check validates 25 skill routes, source hashes, four exact technical-method copies and active relative link closure. It does not execute `game-dev`, install OpenAI Game Studio or prove model routing/player experience. [Lantern Courier](examples/lantern-courier.md) is a fictional design/playtest example, not a playable shipped game.

Run `python3 -B -m unittest discover -s tests -p 'test_*.py'` for executable live-card checks, or `python3 -B examples/check_live_card.py` for the synthetic sample. The helper needs only Python standard library, checks text mechanically and changes no files. It does not run a session, measure player experience, retrieve a rulebook or call a VTT.
