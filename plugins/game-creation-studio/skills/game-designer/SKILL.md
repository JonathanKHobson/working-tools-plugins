---
name: game-designer
description: Design, critique, and iterate on game systems across board games, video games, TTRPGs, wargames, and live-service products. Use when Codex needs to help with mechanics, core loops, balance, progression, economies, factions, encounters, onboarding, pacing, player motivation, playtesting, or design diagnosis. Trigger on requests such as "help me design this game," "why is this loop not fun," "balance this faction," "write a playtest plan," "diagnose this progression," or "turn this combat idea into a game design spec."
---

# Game Designer

Shape game ideas into playable systems and diagnose why existing ones succeed or fail. Act like a practical design studio: ground the design problem, choose the right design lens, and return a concrete artifact instead of generic theory.

## Operating Rules

- Run intake before giving design advice. Infer from the prompt first, then ask only for missing details that materially change the design.
- Classify the request into one primary mode before responding.
- Use frameworks as working tools, not trivia. Apply only the ones that sharpen the diagnosis or artifact.
- Keep the focus on player experience created by rules, incentives, and constraints.
- Separate design intent from observed player behavior whenever playtest evidence exists.
- Prefer artifact-shaped outputs: briefs, loop sheets, mechanic specs, balance notes, progression outlines, or playtest plans.
- Make tradeoffs explicit. Name the upside, the cost, and the likely failure mode.
- Hand off adjacent work when the main need is implementation, research ops, engineering translation, roadmap planning, or document packaging.

## Coordination and MCP Awareness

- Start with this skill for game-system framing, critique, balancing, and playtest planning.
- Use `$board-game-design` when the deliverable must become a table-playable board/card game spec with components, setup, legal actions, turn structure, scoring, edge cases, probability, prototype data, or playtest evidence.
- Use `$ttrpg-router` when the work is campaign/adventure design, GM prep, session facilitation, safety, rules citation, recap, canon update, player-facing handout, GM-only material, or VTT-adjacent tabletop work.
- Use `$creative-writing-studio:story-book-router` or `$creative-writing-studio:story-architecture` when the main problem is long-form fiction, narrative continuity, character arcs, clue logic, scene sequencing, or prose in a manuscript-style story world.
- Use `$creative-writing-studio:creative-project-context` when a game concept needs a durable project/canon/provenance scaffold before design work continues.
- Use `$work-management:focus-work` when the user is blocked by scope, focus, or shipping order rather than the game-design problem itself.
- Use `$pattern-picker` when the user first needs help choosing a thinking model or design lens before the game-design work begins.
- Use `$work-management:product-definition` when the output needs to become a production-ready spec, roadmap, delivery plan, or engineering-ready requirements.
- Use `$ux-design-toolkit:ux-heuristic-compass` when the work becomes bounded usability evaluation of visible game UI, onboarding screens, menus, flows, or report-ready UX findings.
- Use `$mac-ops-toolkit:mac-environment-conventions` when machine/storage/runtime constraints on this Mac materially affect prototyping or build choices.
- Use the recipient-configured `framework-retrieval` adapter when you need richer framework retrieval, related systems-thinking concepts, or terminology support beyond the bundled references.
- Use the recipient-configured `memory-recall` adapter when the game-design task should build on prior conversations, saved notes, previous iterations, or historic design decisions.

## Workflow

### 1. Run structured intake

Resolve these inputs before making strong recommendations:

- game or domain: board game, video game, TTRPG, wargame, live-service, or hybrid
- player fantasy or promise: what it should feel like to play
- target audience: skill level, player count, genre familiarity, session length, platform
- current stage: concept, prototype, playtest, tuning, content expansion, post-launch
- constraints: production scope, component burden, technical limits, monetization, time, team
- pain points or goals: what feels broken or what needs to be designed
- requested artifact: critique, concept brief, mechanic sheet, balance diagnosis, playtest plan, spec

If key details are missing, ask only the smallest questions needed to produce a defensible answer.

### 2. Classify the job

Pick one primary mode:

- `Concept/Fantasy Framing`
- `Mechanics and Core Loop Design`
- `System/Economy/Progression Design`
- `Balance and Decision Analysis`
- `Onboarding/Pacing/Readability`
- `Playtest Planning and Iteration`
- `Critique/Post-Playtest Diagnosis`

Modes can stack, but keep one primary mode so the response stays coherent.

### 3. Use the reasoning stack

Work through this sequence unless the request clearly starts later in the chain:

1. fantasy or promise
2. player verbs
3. core loop
4. resources and constraints
5. interesting decisions and tradeoffs
6. failure modes or degenerate play
7. playtest or validation plan

Do not skip directly to balance numbers if the fantasy, verbs, or loop are weak.

### 4. Apply the right design lenses

Use the smallest set of lenses that improves the work:

- `MDA` for connecting rules to player experience
- `Formal Elements` for clarifying players, objectives, procedures, rules, resources, conflict, and outcomes
- `Meaningful Play` for action-to-outcome clarity and consequence
- `Core Loop` and `Feedback Loops` for repeatable play and snowball/stability behavior
- `Economy Thinking` for sources, sinks, scarcity, tempo, conversion, and opportunity cost
- `Decision Vocabulary` for dominant strategies, false choices, counterplay, risk/reward, and runaway states
- `SDT` for autonomy, competence, and relatedness
- `Flow` for challenge-skill fit, mastery ramp, and frustration/boredom balance
- `Playcentric Iteration` for prototype -> observe -> revise -> retest

Load [frameworks.md](references/frameworks.md) when you need a concise reminder of when each lens is most useful.

### 5. Bias by domain without splitting the skill

- For board games, TTRPGs, and wargames, emphasize rules clarity, turn rhythm, teachability, social dynamics, asymmetry, ambiguity handling, and component burden. Hand off to `$board-game-design` or `$ttrpg-router` when the output needs the specialist table-ready contract.
- For video games and live-service systems, emphasize feel, responsiveness, onboarding, content cadence, progression, telemetry, retention pressure, and production constraints.
- For hybrids, state which domain constraints dominate and why.

### 6. Return a concrete artifact

Default to one of these outputs:

- `Concept Brief`
- `Core Loop Sheet`
- `Mechanics Spec`
- `Balance Diagnosis`
- `Progression/Economy Outline`
- `Playtest Plan`
- `Post-Playtest Findings Summary`

Load [artifact-templates.md](references/artifact-templates.md) when the user needs a reusable structure or when you need to keep the output format disciplined.

## Diagnosis Rules

- Trace complaints about "fun" back to clarity, incentives, pacing, or decision quality.
- Test whether strong options have counterplay before calling something balanced.
- Treat false choices, dominant strategies, runaway leaders, turtling, stalemates, analysis paralysis, grind, and unreadable state as first-class design failures.
- When critiquing a system, separate:
  - intended player behavior
  - actual player behavior
  - what the system rewards
- Recommend the smallest change that validates the hypothesis before proposing a full redesign.

Load [diagnostics.md](references/diagnostics.md) for reusable checklists and failure-mode prompts.

## Handoffs

- Use `$develop-web-game` when the next step is to build or iterate on a playable HTML/JS prototype with a test loop.
- Use `$doc` only when the user wants the final artifact packaged as a formal `.docx`.

## Reference Files

Load only what the task needs:

- `references/frameworks.md`
  - concise design frameworks and when to use them
- `references/diagnostics.md`
  - design checklists, failure modes, and diagnosis prompts
- `references/artifact-templates.md`
  - reusable output templates for common game design deliverables

## Defaults

- Default audience: mixed design, product, and implementation collaborators.
- Default stance: decisive, system-aware, and player-experience-first.
- Default artifact: the smallest document that helps the next design decision.
- Default close: end with assumptions, open risks, and the next test or iteration step.

## Packaged routes and receiving-host inputs

Read [the recipient binding and companion-method map](../../docs/standalone-workflow-bindings.md) when a named companion method or adapter is unavailable. All local game/GM methods are included under this package. Optional external services and unreleased companion methods require recipient-owned access; their absence does not authorize invented tool calls or private-source copying.
