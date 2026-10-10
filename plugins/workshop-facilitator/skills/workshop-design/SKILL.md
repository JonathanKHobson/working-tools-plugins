---
name: workshop-design
description: Create a complete workshop agenda and facilitator run sheet for a defined group outcome, including timing, participation, materials, and contingencies. Also use for a concise “what can this plugin do/how do I get started?” answer; route specific tasks to the matching specialist.
---

# Workshop Design

If asked what this plugin can do or how to start, use the [human guide](../../README.md) to offer an agenda, in-room intervention, or notes synthesis with needed group/context and result. For a defined workshop task, begin directly or route to its specialist; do not require a tour or claim a live Atlas lookup from the manifest alone.

Identify what participants should leave with: a decision, shared frame, tested idea, capability, or working artifact. Infer known constraints from the request; ask only about a consequential missing choice. Distinguish the sponsor's desired outcome from decisions the participants are actually empowered to make.

Read [personal grounding](references/personal-grounding.md) for context-sensitive facilitation defaults and [facilitation evidence](references/facilitation-evidence.md) when choosing a method. For activity details read [method selection](../workshop-activity-selection/references/method-library.md).

## Design the session
Define participants, authority, setting, duration, access needs, materials, and success evidence. Build a sequence in which each activity produces an input for the next. Keep problem exploration, idea generation, evaluation, and commitment distinct when the work requires them. Do not add forced fun or a decision stage to a workshop whose purpose is discovery.

Account for instructions, individual thinking, group work, reporting, transitions, breaks, and closeout. Reserve space for a debrief and a concrete next action. Provide a shorter version that names exactly what gets cut while preserving the core outcome.

For a shared visual board, use the [board sequence in agenda format](references/agenda-format.md#shared-board-sequence). Give one clear active task, evidence on demand, and a completion/next-use cue. Preserve participant wording and source IDs; reveal later work without hiding the constraints or comparisons needed now. A board layout and a facilitator rehearsal are not evidence of participant usability or successful group work.

## Deliver
Produce a timed run sheet with purpose/output, instructions to say, participation format, materials, capture method, and fallback for each segment. Include setup, access options, decision rule where needed, and closing language. Use [agenda format](references/agenda-format.md) and `python3 scripts/check_agenda.py <agenda.json>` from this skill directory for complex schedules. The checker verifies timing, not facilitation quality.

Route a narrow request directly: activity choice → `workshop-activity-selection`; help in the room → `live-workshop-facilitation`; dialogue → `inclusive-group-dialogue`; convergence → `workshop-decision-making`; notes → `workshop-evidence-synthesis`; closure → `workshop-debrief-transfer`; practice → `facilitator-rehearsal`. Do not load every sibling skill for every agenda.


## Scoped Atlas reference

For local facilitation concepts, frameworks, activities or source definitions, read [the scoped Atlas library](../../references/atlas-library.md). Use its relevant-only search and full-source selection before adaptation; human browsing and assistant retrieval share the same source records.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Workshop Facilitator. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
