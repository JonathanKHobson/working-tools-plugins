# AI Workshop Studio v3 planning path

Use this reference only for AI Workshop Studio planning work that names the `v.3 Outline Template`, version `studio-v3-1`, or asks to reconcile the Studio plan, app, and built course. Keep the generic instructional-design router for other work.

## Authority and contract

The portable contract is [ai-workshop-studio-v3-template.json](ai-workshop-studio-v3-template.json). It is an exact copy of the app-owned contract at `lib/authoring/planning/v3-template.json` in the `planning-foundation` worktree. [Contract provenance](ai-workshop-studio-v3-template.provenance.json) records its source and checksum. Treat the app-owned file as the owner and this copy as the offline skill dependency. Run the checker with `--source-contract` when the app checkout is available; a hash mismatch blocks claims that the two implementations are synchronized.

Classify every planning instruction before applying it:

- **Source rule:** required by the selected v3 template, including Step 0 plus Steps 1–6, exactly three objectives, the six task columns, cumulative activity duration, quiz structure, and description length.
- **Research or professional guidance:** supports a design decision but does not rewrite the template. State its scope and limits.
- **Heuristic:** a useful review default, such as practice after roughly three instructional tasks. Do not present it as a universal law.
- **User extension:** a deliberate Studio addition, including Audience, L3 Advanced, richer guidance, whole-activity timing, stable IDs, discussion categories, and delivery scopes.

Do not import rules from older workbook tabs or another course platform merely because they look useful.

## Preserved seven-section structure

Keep these source fields and order. Extensions may add metadata without renaming or displacing them.

1. Step 0, Project Information: Instructor Name; Project Title; Additional Project Information; Difficulty Level; Software/ Tool. Audience and Technical Requirements are Studio extensions.
2. Step 1, Write Your Outcome and Learning Objectives: Project Outcome; Learning Objective 1; Learning Objective 2; Learning Objective 3; Prerequisites. Keep exactly three objectives with stable IDs.
3. Step 2, Your Project: Project Artifact; Real-World Connection; Project Scenario. The artifact is a usable deliverable, not an outcome, activity list, or bundle of learning records.
4. Step 3, Explain What Learners Will Do in Each Task: Task Objective; Task Description; Step-by-Step Learner Actions; Aligned Learning Objective; Task Type; Estimated Time, in that order.
5. Step 4, Design a Cumulative Activity: Cumulative Activity Description. Expand it with situation, inputs, output, permitted help, criteria, time, objective alignment, and an instructor solution without replacing the source field.
6. Step 5, Craft Your End-of-Project Quiz: Task #; Aligned Learning Objective; Assessment Question; Answer Choices. Add author-only answer key, explanation, feedback, and multiple-select instructions as extensions. Each instructional task needs an explicit question link, at least four choices, and feedback.
7. Step 6, Write a Description For Your Project: Guided Project Description, 150–250 words.

## Diagnose, review, and repair

First map existing content by stable field and task IDs. Classify each finding as `missing`, `misplaced`, `contradictory`, `weak`, `unverified`, or `conforming`. Keep source text available while proposing changes.

For substantive fields, record `status`, `evidence/source`, `reviewer decision`, `unresolved issue`, and `proposed change`. Valid decision states are `approved`, `proposed`, `rejected`, `unresolved`, and `needs-review`. Existing workbook text, app text, built content, or an earlier brainstorm is not approval evidence.

Check alignment in both directions:

- Each objective has instruction, practice, and assessment evidence.
- Each task changes the artifact or supplies a necessary capability.
- The cumulative task applies taught capabilities independently and introduces no required new tool, workflow, or concept.
- Each quiz question links to an instructional task and objective; the quiz supports judgment but does not replace evaluation of the artifact.
- Every learner-facing promise in the description is supported by the reviewed plan.

Return a readiness report with exact failures, affected IDs, mechanical checks, judgment calls, approval gaps, and plan/app/course drift. Flag problems; do not silently modify a live course or treat a mechanical pass as instructional approval.

## Timing and delivery scopes

Time orientation, setup, instruction, practice, discussion, cumulative work, quiz, and transitions. A cumulative Step 3 row is a sequence reference to the detailed Step 4 specification. Its own task-row time may be zero and is always ignored in arithmetic. Count the Step 4 duration exactly once for each delivery scope named by the reference row, following that row's required or optional scope. Duplicate reference rows are a schema failure and still contribute the Step 4 duration only once per affected delivery scope.

Keep `full-course`, `live-pilot`, and `self-paced` budgets separate when they differ. The cumulative activity remains 10–20 minutes. It must fit inside a 60-minute live budget only when that cumulative activity is actually included in the live pilot. Do not force the full curriculum into the first 60-minute pilot or treat pilot completion as completion of the full course.

For the current Monday project, the first meeting is a bounded 60-minute pilot. The larger curriculum may extend from AI basics and landscape through small prompt practice, desktop/web setup, plugins, skills, connected apps, Drive/Gmail, and creating and using a skill. Scenario and primary artifact are unresolved and require Kyle's decision. Do not adopt the current packet or an older brainstorm as approval.

## Access and product claims

Name the exact environment. ChatGPT Desktop, Codex Desktop, and Claude are different products with different skill, connector, and file behaviors. Supplied exports, pasted instructions, installed skills, and live connector execution are different routes. Mark a capability `verified-current` only from current evidence; otherwise keep it proposed or unverified and provide an honest manual route when one exists.

## Deterministic checks

Use the checker for exact structure, field/column order, title and description limits, objective/task/question references, cumulative duration, timing arithmetic, and current-evidence dependency claims:

```bash
python3 scripts/check_studio_v3_outline.py OUTLINE.json
python3 scripts/check_studio_v3_outline.py OUTLINE.json \
  --source-contract /path/to/planning-foundation/lib/authoring/planning/v3-template.json
```

The checker accepts the fixture representation documented by the complete fixture in the project receipt. It cannot approve a scenario, authenticate tool access, establish assessment validity, or prove learning effectiveness. Review those judgments directly.
