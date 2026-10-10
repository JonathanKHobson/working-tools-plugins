# Agenda JSON

The [60-minute example](../assets/agenda-example.json) is a fictional discovery workshop. Timings are proposed, not field-tested.

Use `duration_minutes` and an ordered `segments` array. Every segment has `id`, `start`, `end` (elapsed minutes), `kind`, `title`, `purpose`, `output`, `instructions`, and `fallback`. Kinds are opening, activity, transition, break, debrief, closeout. Times are finite numbers, begin at zero, are contiguous, and end at the stated duration. Represent transition and break time explicitly; for a break, an output such as readiness to resume is sufficient. The final segment must be closeout.

Run from this skill folder:

```bash
python3 scripts/check_agenda.py assets/agenda-example.json
```

The script checks IDs, intervals, required fields, and explicit closure. It does not prove the room can complete the task in that time or that the activity fits the group. Rehearse the agenda and preserve the core output when adapting it.

## Shared-board sequence

For a FigJam or similar collaborative board, pair each agenda segment with its actual section/link, current prompt, contribution location/mode, time, completion cue, and next use of the output. This is an extension of the run sheet, not a requirement to create another planning artifact or change the JSON checker. Build only the stages the group's outcome needs. An eight-stage route or a three-option shortlist can be a starting design, not a universal requirement.

Keep three layers distinct: small orientation/route; current work with necessary evidence; indexed reference and unresolved questions. Put the question bank and method detail in Reference, preserving exact source wording/IDs and providing relevant excerpts near the task. Show one active assignment instead of every possible exercise. Keep decision authority, boundaries, constraints, and criteria available from arrival. Related alternatives and evidence stay visible together while comparing them.

Rehearse transitions as: summarize the output, reveal the next task, check that required context is available, then offer a section link and optional follow. Hide completed work only when it is no longer needed; keep a reliable return route. Native hiding is presentation control, not confidentiality. Do not promise private ideation or anonymous voting without the actual mechanism being verified. Keep confidential facilitator notes outside the shared board. Delegate editor mechanics to the current Figma provider and its own capability checks.

Use one optional arrival activity only when it teaches a contribution route or helps the group start. Include Pass, typed/scribe/non-drag access, and no mandatory drawing, camera, disclosure, or music. Practice that route before substantive work. Do not add a menu of games. Independent notes before group display can reduce immediate influence; explain how and when contributions become visible.

Preserve raw statements, distinct ideas, contradictions, and minority concerns when clustering. Add labeled summaries linked to their source IDs. Expand a linked continuation area for overflow rather than dropping contributions or shrinking all text. A parking item needs a revisit point or an explicitly unassigned owner, not just a cheerful label.

For decision workshops, pass candidate IDs into a shortlist with reasons, compare on common criteria, record a choice or explicit deferral, and then seek accepted next steps. Use [decision patterns](../../workshop-decision-making/references/decision-patterns.md) for that handoff. Discovery workshops still stop at their authorized findings/options.

When time contracts, trim redundant reporting and optional activities rather than rushing an unresolved decision. A shorter decision session may require prepared evidence and candidates; if these are missing, make clarification or a recommendation the honest output. For larger groups, budget small-group synthesis and report-back rather than merely multiplying input cards.

Close in review mode: completed work, decisions, and unresolved items must be readable without a facilitator revealing the next section. Reconcile the participant text companion with the actual record. Reset only an unused master or authorized session copy, never the historical session. Rehearse the real laptop-scale task and access route before calling setup ready; record which checks passed, failed, were unavailable, or were not tested.

Evidence: [FigJam handoff adoption and limits](facilitation-evidence.md#collaborative-board-handoff). These are design recommendations, not measured effectiveness claims.
