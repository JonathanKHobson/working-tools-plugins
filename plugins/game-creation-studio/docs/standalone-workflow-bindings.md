# Complete game and GM methods, recipient inputs and optional companions

All fifteen added first-party standalone methods retain their full operative bodies, references, test scenarios and the real live-card helper. Select a local method from [the route map](routes.json) or its package-local skill directory. Native hosts may expose it as `game-creation-studio:<skill-id>`; a missing host registration can use the same Markdown source. No script installs a service or configures a host.

## Local workflow routes

- [`board-game-design`](../skills/board-game-design/SKILL.md): playable board/card rules, components, probability and evidence.
- [`game-designer`](../skills/game-designer/SKILL.md): cross-domain design lenses, systems and concrete design artifacts.
- [`debrief-canon-maintainer`](../skills/debrief-canon-maintainer/SKILL.md): source-linked actual-play recap, proposed canon patches and next-session hypotheses.
- [`improv-roleplay-coach`](../skills/improv-roleplay-coach/SKILL.md): bounded rehearsal and low-pressure roleplay practice.
- [`live-table-director`](../skills/live-table-director/SKILL.md): immediate compact live GM card with exact words, signals and stop condition.
- [`npc-performance-director`](../skills/npc-performance-director/SKILL.md): playable NPC goals, performance handles, information tiers and exit conditions.
- [`pacing-scene-director`](../skills/pacing-scene-director/SKILL.md): scene pressure, clocks, clue movement and finale protection.
- [`player-facilitator`](../skills/player-facilitator/SKILL.md): observable participation, spotlight, conduct and multiple response modes.
- [`professional-public-gm`](../skills/professional-public-gm/SKILL.md): paid/public table preflight, welcome, time discipline and service recovery.
- [`rules-teaching-coach`](../skills/rules-teaching-coach/SKILL.md): concise fiction-first rules teaching with source/ruling labels.
- [`safety-accessibility-facilitator`](../skills/safety-accessibility-facilitator/SKILL.md): consent, access, live content edits and private follow-up boundaries.
- [`personal-gm-style-adapter`](../skills/personal-gm-style-adapter/SKILL.md): optional removable style layer after source, agency and safety constraints.
- [`ttrpg-router`](../skills/ttrpg-router/SKILL.md): campaign/adventure prep, privacy, rules citation and table-ready artifacts.
- [`gm-roleplay-router`](../skills/gm-roleplay-router/SKILL.md): smallest specialist selection across live, prep, teach, coach and debrief.
- [`daggerheart-adapter`](../skills/daggerheart-adapter/SKILL.md): original Daggerheart adjudication guidance with current official source checks.

## Recipient input authority

Supply your own authorized current rule sources, campaign canon, actual-play notes and table preferences. Keep player-facing, GM-only and sensitive material separate. The package contains original source-aware Daggerheart guidance, not SRD text, a rulebook, cards, artwork, stat blocks or a claim to an official publisher affiliation. Verify current official edition/errata/license before authoritative answers. Labels remain official, table-ruling or verify-after-play. Missing source status permits a clearly labeled reversible ruling; it never permits invented citations.

The personal style adapter is optional authored example guidance, with an explicit remove-this-layer version. Your actual preferences, player details, accommodations and private feedback are inputs you control; no personal canon or voice samples ship here. Write permission follows the user's scoped authorization, including authorization already supplied. Propose reviewable local patches when useful; do not confuse that with an executed live service edit.

## Optional method companions

The original methods name Creative Writing/Story Atlas context, story architecture, originality/provenance, show-versus-tell, publishing and communication methods; UX visual integration/evaluation; Work Management focus/product specification; a pattern selector; and external browser-game/document authoring tools. They are optional specialist routes, not bundled source or a promise those packages are publicly available. Some original studio families remain held for unrelated operative-source rights. Use an available recipient-owned method only when it materially helps the task. Otherwise continue with the complete included workflow and the supplied project files: a table-ready run sheet, rules contract, NPC card, proposed canon patch or source-aware debrief. For live description, the included live method already defines SHOW one concrete cue, TELL one necessary clarification, ASK one contribution question and CUT at the scene transition. Do not invent an adapter call or claim absent companion output.

## Optional service roles

`framework-retrieval` supplies additional design lenses; `memory-recall` retrieves authorized prior game decisions. Campaign/Story Atlas, TTRPG Compass and VTT services can read or update recipient-selected records only when an actual tool is available and the action is authorized. Knowledge Atlas, TTRPG Compass, P2P GM MCP and named VTTs in the retained source are examples of external integrations, not endpoints installed here. Discover their actual current tool schema, inspect harmless reads first and confirm returned source identity. If absent, work from supplied Markdown/local artifacts and keep proposed patches reviewable.

[Recipient bindings](../examples/recipient-bindings.example.json) records roles and source authority without secrets or personal host paths. It is a documentation example, not an executable service configuration. Set provider and tool names to what your receiving host actually exposes. Credentials belong in that provider's supported secure configuration. Local text workflows and the live checker need none of these adapters.

## Real helper

`skills/live-table-director/scripts/check_live_output.py` reads a run card from stdin, checks seven markers, the 140-word ceiling and a bounded diagnostic/shaming-label pattern, then writes a result to stdout/stderr. It changes no files, makes no network request and performs no game or VTT operation. Mechanical success does not prove tone, safety, player consent, agency, actual table response or general accessibility. The full source scenarios are preserved; package tests exercise valid and deliberately invalid synthetic cards.
