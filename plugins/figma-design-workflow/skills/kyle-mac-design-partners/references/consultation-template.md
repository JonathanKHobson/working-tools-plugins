# One-decision design consultation

Adapt this into a short natural-language prompt; omit irrelevant fields.

“Help decide [specific design question] for [audience completing task]. The current artifact is [selected file/screenshots]. Here are verified facts and accepted decisions: [brief list]. These are unknown: [gaps]. At anchors [IDs], the observed issues are [facts]. Preserve [identity/navigation/content]. Constraints are [stack, format, viewports, accessibility, scope]. Provide [prioritized critique / two or three distinct options / one mockup]. Explain the main tradeoff and assumptions. Do not invent results, client history, or user research. This request is [critique only / file edits limited to verified scratch workspace].”

For code/mockups add:

- Verified local workspace and permitted files; no edits to the owning Codex checkout.
- Required real states and interactions, plus behaviors allowed to remain simulated.
- Export format and expected path; use local handoff if requested.
- Deliverable: actual files, concise change summary, remaining gaps, and how to preview.

## Return packet

- Partner and actual mode/model used; current plan limitation if relevant.
- Decision requested; accepted recommendation and reason.
- Artifact location and what was verified there.
- Suggestions vs source facts vs accepted implementation changes.
- Remaining implementation, testing, and visual anchors for Codex.

Keep the transcript and private screenshots in the project's review area, marked temporary where applicable. Preserve source evidence. Do not save consultation content into reusable skill instructions.
