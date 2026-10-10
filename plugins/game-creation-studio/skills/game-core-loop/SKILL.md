---
name: game-core-loop
description: Use to turn a game idea into a playable core loop, player verbs, stakes, feedback, and a testable design hypothesis before choosing content scale or an engine.
---

# Game Core Loop

Start from the player's intended experience and a single observable choice they repeat. Ask for a missing genre, audience, or platform only when that answer changes the loop; otherwise state a working assumption and proceed.

1. Write the player fantasy in one sentence and name the verbs the player can perform. Distinguish what the player controls from what merely happens on screen.
2. Describe one loop as **state → choice → action → feedback → changed state → next choice**. Give a concrete 30 to 90 second example with the information the player sees at each choice. Make success and failure legible.
3. Identify tension: scarce resource, time, position, risk, uncertainty, or competing goal. Remove any rule that adds bookkeeping without a meaningful choice.
4. Specify controls and immediate feedback for each main verb. Include a first successful action before explanatory text grows. Identify an idle state, recovery after failure, and the moment a player can stop or try again.
5. Give one falsifiable playtest hypothesis: what a new player should attempt or understand without coaching, and the observation that would disprove the design. Avoid claiming fun from a written concept.

Deliver a concise loop diagram, a one-run sequence, the smallest prototype needed to test it, and 1 to 3 design uncertainties. Route the slice to [prototype scope](../game-prototype-scope/SKILL.md). If coding a browser game, use official OpenAI Game Studio's `game-studio` for stack selection and `web-game-foundations` for shared architecture; then its engine specialist. Preserve the player's goal through that handoff.

If an existing build is supplied, observe a real run or supplied evidence before redesigning its loop. Separate the observed player path from an explanation of why it fails; test the strongest alternate explanation, such as unclear feedback rather than a weak mechanic. A concept sheet is design evidence, not player evidence.
