---
name: gameplay-systems
description: Use to design or repair game rules, state transitions, progression, economy, balance, difficulty, saves, or multiplayer rules with testable invariants.
---

# Gameplay Systems

Start with the player decision the system should create, then inspect the current rules and data. Name observed behavior separately from the suspected balance cause.

1. Model inputs, state, transition, and visible output for the smallest affected system. Define invariants such as legal resource ranges, turn order, spawn limits, victory conditions, and save restoration. Draw a simple state table when a prose rule leaves ambiguity.
2. Identify interactions with neighboring systems: input, physics, scoring, level flow, UI, audio, and persistence. Put balance constants in the project's established configuration home; keep deterministic rule logic separate from presentation when that project architecture supports it.
3. For progression or economy, simulate a few representative player paths: cautious, aggressive, novice, and expert. State assumptions and compare resource inflow/outflow, time to reward, and possible dead ends. Use this to choose an initial tuning range, not to declare balance solved.
4. Implement or specify a minimal transition test for consequential edge cases: zero resource, simultaneous events, reset, pause/resume, save/load, and failure recovery. For multiplayer, also test authority, reconnect, and disagreement resolution within the chosen network model.
5. Observe at least one player session or real run before recommending broad tuning. Record exact build, scenario, and what the player attempted. Change one rule family at a time, then check the original decision and adjacent regressions.

Deliver the rule table or code change, acceptance cases, tuning values with their rationale, and unresolved player questions. Browser execution routes to official OpenAI Game Studio's `web-game-foundations` plus `phaser-2d-game`, `three-webgl-game`, or `react-three-fiber-game` according to the established stack. Do not present a spreadsheet simulation as a playtest result.
