# Handoff contract: lane02 (human systems) → lane01 (interactive dashboards and widgets)

**Status:** proposed. Lane01's packet didn't exist when this was written (`packets/` was empty), so field names below are semantic, and lane01 maps them onto its own schema. This contract adds human-performance requirements and their rationale. It doesn't replace `skills/dashboard-design/SKILL.md` or its `visualization-contract.md`; the contract wasn't read here, so the mapping is unresolved.

## 1. What lane02 supplies

- Decision cards HS-01…HS-07 (`patterns.md`) and the staged reference `proposed/human-systems-decisions.md`.
- PCEA worksheet (`examples/pcea-task-worksheet.md`) for task analysis of any widget or dashboard flow.
- Worked critiques on the shared benchmark facts (`examples/case-1…3`).

## 2. What lane01 must carry in every dashboard or widget spec

Each requirement names the lane02 card that justifies it and the shared benchmark task that exercises it (`shared/benchmark-brief.md`).

| # | Requirement | Card | Benchmark task | Acceptance check |
|---|---|---|---|---|
| 1 | **Carried-item count** for the main comparison task, before and after the design (target: nothing the person must remember across a view change) | HS-02 | T2 | Walkthrough lists carried items; compared items share units and scales and are co-visible |
| 2 | **Visible scope and freshness** wherever results appear: active filters, range, "n of N items", last updated. Also required in empty states | HS-02, HS-06 | T3, T5 | Scope is visible in default, filtered, empty and error states; Reset is always reachable |
| 3 | **Rating with its base** ("4.6 (5 responses)") every time a rating is shown; no significance language | HS-02 | T2 | Every instance inspected |
| 4 | **Feedforward for scenario and analytic controls:** a preview of what changes, where and by how much, before commit; scenario values visibly marked; source values stay visible | HS-03 | T4 | Each scenario control states its effect; restore returns every value; no silent overwrite |
| 5 | **Mechanism per consequential action:** each is mapped to prevent, confirm or undo; scenario changes are reversible without a modal; applying to source data requires review with a consequence list | HS-05 | T4 | Action inventory with a mechanism column; no generic "Are you sure?" on frequent actions |
| 6 | **Resumption:** drafts and scenarios survive navigation, timeout and re-authentication, and come back with a cue (pending changes, next item) rather than silently | HS-04 | T4, T5 | Forced interruption walkthrough |
| 7 | **Pointer and keyboard:** targets meet WCAG 2.2 2.5.8 or its spacing exception; destructive actions are separated from frequent ones; every drag has a single-pointer alternative (2.5.7); core tasks can be completed by keyboard at 390 px | HS-01 | T6 | Hit-area measurement; keyboard-only run at 390 px |
| 8 | **Announced status:** filter results, scenario state, errors and completion are exposed as status messages (4.1.3) | HS-03 | T3–T5 | Screen-reader or accessibility-tree check (tool-dependent; mark as not run if unavailable) |
| 9 | **Workload rationale** for density decisions: name the dimension and the use duration (glance, session, shift) when adding or removing context | HS-06 | T1 | Each simplification says what moved where |
| 10 | **No emotion claims** in dashboard critiques without an evidence type | HS-07 | all | Claim audit |

## 3. What lane01 owns and lane02 does not

- Chart encoding choice, visual grammar, widget taxonomy, art direction, renderer and data semantics.
- Any numeric layout values (panel sizes, density, breakpoints) beyond the WCAG floors cited above.
- Choosing among the structurally different alternatives in case 1 (comparison workbench, exception-first monitor, scenario sandbox). Lane02 only notes the condition each one suits.

## 4. Claim ownership across lanes

The following claim types in any lane's output should either cite a lane02 card ID or be labelled unverified:

- **Perception and attention:** salience, noticing, grouping *as it affects task performance*. Gestalt and visual composition claims belong to lane03, but when a lane03 composition change is justified by "users will notice X", that is a lane02 claim.
- **Memory and cognition:** recall, recognition, comparison, mental models ("Matching Mental Models", Kyle's U09 heading).
- **Action and motor demand:** pointing, dragging, keyboard, touch, reach.
- **Errors and recovery:** prevent, confirm, undo, resumption.
- **Feedback and feedforward.**
- **Workload** in any dimension.
- **Emotion** as evidence (see HS-07). Lane04 and lane05 own *rhetorical* uses of emotion. They must not cite emotional inference as user evidence, and research instruments must stay neutral (case 3).
- **Social and physical context:** collaborative use, shared devices, situational impairment. There's no primary source for collaborative activity in this pass, so these remain hypotheses for any lane (`unresolved.md`).

## 5. Interface between the packets

- **Lane01 → lane02:** a list of the widget and dashboard flows lane01 will prototype, each with its task steps. Lane02 (or Codex using the worksheet) returns PCEA rows and card-based findings.
- **Lane02 → lane01:** the requirements table above plus card IDs to cite in lane01's rubric under "accessibility" and "task fit".
- **Conflict rule:** if a lane01 aesthetic choice conflicts with requirements 2, 4, 5, 7 or 8, the requirement wins, because these are correctness, integrity and accessibility gates (research contract, "Safety, honesty, and essential usability are gates"). Other conflicts are tradeoffs; record them in the spec.
