# Product task context

Use when starting a product design task, resolving competing source instructions or recovering an interrupted prototype. This complete UX-owned method replaces method-pack setup dependencies; it does not require a questionnaire before a well-specified change.

## Read the current task before expanding it

Write the requested outcome in one sentence, including the surface, user action and requested end state: critique, editable mockup, local prototype, implementation, preview or published page. Establish audience, primary task, environment and success condition. Infer routine decisions from the prompt and existing project. Ask only about an unresolved choice that would materially change the result; continue independent work while it is unresolved. Do not turn a screenshot correction into research, brand strategy or an app rewrite.

Inspect the owning project map, current entrypoint, related shipped screen, components, tokens, source assets and existing checks. Distinguish authored sources from generated exports. Record which evidence governs content, visual appearance, behavior and constraints. Read connected issue/design notes only when relevant. A URL or screenshot has authority only for what it actually shows; private accounts and unrelated files are not part of this method.

## Context record

Reuse an existing brief, issue or DESIGN.md when possible. A compact working record can be embedded in the deliverable rather than creating a new registry.

| Field | Example for a fictional appointment tool |
| --- | --- |
| Outcome | Prototype selecting and confirming an appointment |
| User/task | Returning patient finds an available slot and confirms it |
| Surface/environment | Existing mobile web flow, keyboard and touch |
| Sources | Supplied screenshot for layout, issue for confirmation rules, existing tokens for type/color |
| Keep | Provider name, availability semantics, cancellation wording |
| Change | Date selection and confirmation feedback |
| Defer | Account redesign and billing |
| Evidence/limits | Screenshot shows one selected date; error/loading state unobserved |
| Acceptance | Select a slot, submit once, see confirmed outcome, recover from failed submission |
| Stage | Local prototype with fictional slots; production availability unconnected |

Do not invent participant preferences, product analytics, technical integrations or business targets to fill blanks. Mark assumptions and describe how they would be checked. Reuse already supplied brand choices; existing organization/project rules govern. Source precedence comes from the task and project, not a generic template.

## Alternatives and implementation handoff

When a consequential interaction remains unresolved, compare a small number of feasible options against the same task, constraints and strongest failure case. Include tradeoffs, evidence, reversibility and what would change the recommendation. For example, a calendar grid supports familiar spatial selection but can hide unavailable times; a dated list supports scanning and narrow viewports but loses month overview. Choose using actual scheduling needs and test the chosen path. Read [decision alternatives](decision-alternatives.md) for deeper evaluation; do not run simulated personas as user research.

Define the screen/state contract before building: route/entry, input/output, primary action, loading/empty/error/success, navigation/back, disabled/repeated actions, persistence and accessibility. Use [experience methods](product-experience-methods.md) for IA, flows and wireframes, [prototyping](product-prototyping.md) for a runnable artifact, and [usability testing](usability-testing.md) for observed participant tasks. Research framing can use the complete [UX Oracle method](../../../libraries/ux-oracle/SKILL.md) and its relevant support under current evidence constraints.

## Resume and closeout

On return, inspect the current source and actual running/hosted state. Reuse unchanged evidence only when the artifact and relevant context match. Find the last verified step, unresolved issue and next necessary action. A stale note saying “deployed” is not live verification. Preserve another task's resources and user work. Stop only task-owned temporary servers/helpers after use; intentional continuing previews need an explicit handoff.

Completion requires the requested end state, the changed task path, relevant rendered anchors, material limitations and a usable artifact/link. Record what was prepared, saved, previewed or published as distinct states. The prototype method provides the execution and delivery checks; current hosting tools own release mechanics.

## Save, inspect and update design sources

For an explicit request to save reusable sources/preferences or inspect what this project remembers, use the original [design-source context helper](../../../scripts/design_source_context.py). Keep the record in the user's owning project, with source assets beside it; do not establish a second global memory system or write private bindings into this shared plugin. This optional workflow has no automatic setup gate.

`python3 <plugin-root>/scripts/design_source_context.py --record <project>/design-sources.json init` creates only the explicitly named record; `list` reads it, reports `missing` without creating it and returns its source entries/preferences. `add --id booking-source --category screenshot --label "Booking source" --target <path-or-url> --note "Appearance authority; mobile state unknown"` records a source with UTC date and status. Categories cover product URL, Figma, screenshot, codebase, component docs, tokens, brand/assets and general context. `import-image --id ... --label ... --source <local-image>` copies a specifically selected bounded image into the record's own asset folder without overwriting another file. `set-preference --key browser --value ...` and `remove --id ...` update only the named record. Use `--replace` only for an explicitly requested replacement.

Before writing, check the selected path, ownership and actual permission. The helper validates record structure, refuses silent ID replacement, uses an exclusive mutation lock and atomic write, retains the immediately previous valid record, and reports unavailable storage as a failure. It does not browse references, install software, call connectors or prove source accessibility. Read only relevant saved entries during design work; current task instructions/source override stale saved preferences. Resolve relative local targets against the record's directory and inspect the actual file/URL when needed. Missing sources and placeholders are not facts.

Keep secrets, credentials, private tokens and copied customer data out of the record; minimize source screenshots and ensure saving them is within the user's request. A local copied screenshot proves saved bytes only. A successful `list` readback confirms persisted entries/preferences, not future source availability or publication. If persistence is unavailable, continue with conversation/task context and state that it was not saved. Setup-only or recall-only requests do not begin a design/build/audit.
