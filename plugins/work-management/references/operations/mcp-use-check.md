## MCP Use Check

Use when enabling or relying on a Codex MCP for a task.

1. Confirm the MCP is needed for this task. The automation-safe baseline is
   exempt from temporary-use cleanup: `arxiv-scout`, `critical-compass`,
   `discord_digest`, `knowledge_atlas`, `shareables`, and
   `kyle_second_brain`.
2. Enable only the MCPs required for the current work.
3. Use the narrowest tool that answers the question.
4. Keep MCP output tied to the deliverable, not exploratory sprawl.
5. Before signoff, disable MCPs enabled for the task unless Kyle explicitly asks
   to leave them on. Never disable the automation-safe baseline as routine
   cleanup.
6. Report what was enabled, what evidence it provided, and whether it was
   disabled again.


## Compass selection cues

Select from the requested outcome, not an exact tool-name mention. These are routes to maintained owners, not proof that a provider is connected.

| Current need | Existing owner | Smallest useful use | When to surface the deeper option |
|---|---|---|---|
| Interface task flow, usability problems, release/handoff evidence | `ux-design-toolkit:ux-heuristic-compass`, reached from Design Studio | Bounded evidence-backed triage with the actual UXHC quick-scan tool when callable | A graded heuristic breakdown, comparison, or reusable audit report would change the next decision |
| Critique a claim, essay, paper, or consequential argument | `reasoning-studio:critical-reasoning` | Claim stress test or supplied-text quick scan through Critical Compass | Council perspectives, dimension scores, a report, or human checkpoints are useful/requested |
| Diagnose a failing prompt, preserve requirements, or prepare a complex prompt | `prompt-playbook-studio:prompt-playbook` | Select the matching Prompt Compass route/diagnosis/preflight via its existing handoff | Guided refinement or evaluation would resolve uncertainty beyond a simple wording edit |

Name the expected result briefly when using a Compass helps the human follow the work: for example, “I’m using UXHC to connect these navigation issues to evidence and concrete fixes.” For an optional deeper review, explain its benefit and scope in ordinary language. Avoid repetitive capability menus or a full audit for a typo, routine fact, or one-line reply.

Before use, discover the actual tool and read only its owner's relevant contract. UXHC starts with compact `get_started(topic="brief")`; Critical and Prompt depth follows their existing integration/handoff contracts. A skill being installed, a tool being exposed, and a successful operation are different states. If unavailable, say which capability is missing and continue the authorized task with clearly labeled manual analysis; don't claim a Compass result, fabricate its score, duplicate registration, or silently change host configuration.

For human review, show any required findings preview before questions. Tool-call acceptance is not proof of visibility. Use the supported input surface and acknowledgment; a visible control is not a stored answer. Preserve actual human answers separately from explicitly authorized sample answers. Widgets present evidence and choices; canonical Compass scoring, validation, consent and checkpoint state remain authoritative. Keep routine retrieval separate from deliberately opening a human-facing widget.
