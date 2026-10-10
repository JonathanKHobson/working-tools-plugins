---
name: board-game-design
description: Design, specify, critique, prototype, and playtest board and card games, including experience pillars, components, setup, state, legal actions, turn structure, scoring, ties, rules clarity, probability, simulation, balance evidence, accessibility, teachability, and iteration logs.
---

# Board Game Design

Use this skill for board games, card games, tabletop prototypes, print-and-play concepts, rules documents, components, probability, balance, and playtest analysis. Use `game-designer` for broad cross-domain game strategy; use this skill when the artifact must become playable at the table.

## Intake

- Experience promise: what should play feel like?
- Player count, duration, age/experience, table context, accessibility needs.
- Components: cards, board, tokens, dice, hidden information, player aids, app support.
- Current stage: concept, rules draft, prototype, playtest, balance pass, blind test, production prep.
- Known constraints: component count, printability, randomness, complexity, theme, table footprint.

## Rules Contract

Every serious rules output should define:

- objective
- components
- setup
- state
- legal actions
- turn/round/phase sequence
- timing windows
- end condition
- scoring
- ties
- examples
- edge cases
- glossary
- hidden/open information
- solo/team/co-op variants if applicable

## Analysis Lenses

- Meaningful decisions: options, tradeoffs, information, consequence.
- Degenerate strategy: dominant options, stalemates, turtling, runaway leaders, kingmaking, analysis paralysis.
- Economy: sources, sinks, tempo, conversion, scarcity, hoarding, catch-up.
- Probability: dice/cards/bags, expected value, variance, tails, event frequency, feel vs math.
- Playtest evidence: observation before interpretation.
- Accessibility/teachability: component legibility, color independence, memory burden, downtime, text density, first-turn clarity.

## Evidence Levels

Attach evidence level to balance claims:

- intuition
- hand calculation
- exhaustive enumeration
- stochastic simulation
- automated-agent play
- designer playtest
- external observed playtest
- blind playtest

Do not state that a game is balanced unless the evidence level supports the claim.

## External Patterns Harvested

- Squib: data-driven print-and-play thinking, component generation from tables, repeatable outputs.
- boardgame.io: explicit turn/state/phase/move/log model.
- OpenSpiel: formal games, policies, evaluation, and agent-play caution.
- Hypothesis/Z3/OR-Tools: property, constraint, and optimization tests where useful.
- dyce/Icepool: dice and probability modeling patterns.

These are references, not assumed local installs.

## Output Contract

```markdown
## Board/Card Game Spec
- Promise:
- Players/duration:
- Components:
- Setup:
- Turn structure:
- Legal actions:
- End/scoring/ties:

## Design Diagnosis

## Probability / Balance Notes
- Evidence level:

## Playtest Plan
- Hypothesis:
- What to observe:
- Success/failure signals:

## Open Risks
```

## Packaged routes and receiving-host inputs

Read [the recipient binding and companion-method map](../../docs/standalone-workflow-bindings.md) when a named companion method or adapter is unavailable. All local game/GM methods are included under this package. Optional external services and unreleased companion methods require recipient-owned access; their absence does not authorize invented tool calls or private-source copying.
