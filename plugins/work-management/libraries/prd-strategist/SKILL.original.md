---
name: prd-strategist
description: Turn product ideas, PRDs, feature plans, roadmaps, and delivery requirements into scoped, decision-ready product documentation. Use when Codex needs to help with PRDs, product specs, MVP planning, user stories, functional requirements, non-functional requirements, acceptance criteria, KPIs, OKR alignment, rollout plans, feature flags, risk matrices, traceability matrices, RACI, stakeholder maps, release planning, API contracts, observability requirements, or prompts like what should I build first, help me scope an MVP, write a spec, write user stories, or explain this to a developer. Do not use for UI copy-only work; use ux-writer. Do not use for narrow terminology translation into engineering language; use plain-to-dev. Use doc only when the user wants a formal .docx deliverable.
---

# PRD Strategist

Turn fuzzy product thinking into clear, scoped, execution-ready planning artifacts. Use this skill to structure discovery, define requirements, phase delivery, and produce planning outputs that executives, designers, engineers, and QA can all act on.

## Operating Rules

- Lead with the smallest useful artifact. Do not default to a full PRD if the user only needs a one-pager, MVP scope, feature brief, or ticket-ready breakdown.
- For implementation-affecting changes where chat history is too loose, use a lightweight change packet: proposal/why, requirement scenarios, design notes, tasks, verification, and archive/decision. Keep it small; do not install or invoke an external spec CLI unless the user explicitly approves that separate lane.
- When the change packet should exist on disk, use the local OpenSpec-inspired
  scaffold script instead of hand-building folders:
  `python3 ${PLUGIN_ROOT}/libraries/prd-strategist/scripts/create_change_packet.py`.
- Use the Write -> Task -> Plan method for every request.
- Ask or infer only the information that materially changes scope, sequencing, metrics, or delivery risk.
- Keep recommendations decisive. Flag assumptions and open questions explicitly instead of hedging.
- Treat non-functional requirements, rollout, observability, privacy, and rollback as first-class planning concerns.
- Treat planning actions as fluid, not locked phases. It is valid to explore,
  propose, write tasks, verify, sync decisions, or archive a change in the order
  the work actually needs, as long as the current artifact and stop condition
  are explicit.
- For fuzzy app ideas, beginner builders, or AI-built project checkups, borrow
  the `$vibe-check` pattern: identify the struggling moment, tag evidence as
  `seen it` / `hunch` / `guess`, score Pain versus Served, and define V1 as
  one differentiator plus required table stakes.
- For startup/product ideas, borrow the gstack office-hours forcing sequence:
  demand reality, status quo, desperate specificity, narrowest wedge,
  observation, and future-fit. Push for specific people, workflows, dollars,
  time, consequences, and current workarounds before expanding scope.
- When a user explicitly asks to think bigger, use a visible scope mode:
  `Expansion`, `Selective Expansion`, `Hold Scope`, or `Reduction`. Do not
  silently add or remove scope; surface each expansion as an opt-in decision.
- When multiple changes are active, keep a tiny change ledger with status,
  owner surface, dependencies, verification, and archive/sync state so context
  switches do not blur decisions.
- Stay in product strategy and delivery planning. Use `$ux-writer` for microcopy and `$plain-to-dev` for narrow developer-language translation.
- Use `$doc` only when the user asks for a formal `.docx` artifact or review-quality document packaging.

## Coordination and MCP Awareness

- Start with this skill for product and delivery planning; do not immediately escalate to another skill or MCP unless it materially improves the plan.
- Use `$focus-ops-manager` when the user is really asking for priority direction, accountability, or which deliverable to ship now.
- Use `$pattern-picker` when the user is stuck on how to think about a problem before planning, or when framework selection is itself the task.
- Use `$plain-to-dev` when a concept needs precise engineering language or buildable requirement translation beyond normal PRD structuring.
- Use `$ux-heuristic-compass` when the plan depends on bounded interface evaluation, UX severity findings, launch-readiness review, or report-ready UX critique.
- Use `$frontend-ux` when the planning work needs implementation-aware frontend UX constraints, state coverage, or accessibility guidance in code-facing decisions.
- Use `$mac-environment-conventions` when machine/storage/runtime constraints on this Mac materially affect the plan.
- Use `knowledge_atlas` when you need richer framework, pattern, glossary, standards, or related-concept retrieval than the skill alone can provide.
- Use `kyle_second_brain` memory recall when the user wants the plan grounded in prior conversations, previous specs, saved notes, or historical decision context.
- Use the `figma` MCP only when the planning decision depends on a specific Figma file, node, or design context.

## Workflow

### 1. Classify the job

Pick the lightest artifact that solves the request:

- `PRD`: full planning document for a feature, product, or release.
- `Feature spec`: narrower buildable spec for one capability.
- `MVP scope`: what ships now, later, and never.
- `Roadmap`: phased or slice-based delivery plan.
- `Requirements pack`: user stories, FRs, NFRs, ACs, and dependencies.
- `Delivery governance`: rollout, KPI plan, RACI, risk matrix, ADR inputs, traceability.
- `Change packet`: compact planning record for a change that needs traceable proposal, requirements, design notes, task steps, verification, and final decision/archive.
- `Exploration note`: lightweight investigation record before a change is ready
  for proposal, useful for unclear requirements, performance/debugging,
  architecture options, or competing approaches.
- `Beginner product blueprint`: plain-language plan for a nontechnical or
  AI-assisted builder, including first working version, glossary, cost/free-tier
  assumptions, deployment/secrets basics, growth loop, and build checkpoints.
- `Office-hours diagnostic`: short product interrogation that identifies the
  painful workflow, current workaround, buyer/user specificity, wedge, observed
  surprises, and why the timing improves the product rather than only the hype.

If the user asks for a document file, keep the planning workflow here and hand off final packaging to `$doc`.

### 2. Gather context in small batches

Resolve the minimum inputs needed to make the plan real:

- product or feature name
- one-line elevator pitch
- target user or buyer
- problem or opportunity
- business goal and user outcome
- constraints: time, budget, staffing, compliance, platform, dependencies
- in-scope and out-of-scope boundaries
- approval or delivery context: draft, review, implementation, release

Ask 3-5 high-value questions at a time. If the user is vague, make a reasonable default assumption and label it.

### 3. Run Write -> Task -> Plan

#### Write

- Start with the one-line pitch and the problem before proposing scope.
- Explain why the work matters now.
- Keep sections outcome-first and audience-aware.
- State recommendations clearly and separate facts, assumptions, and open questions.

#### Task

- Break work into independently understandable units.
- Assign stable IDs:
  - `US-###` for user stories
  - `FR-###` for functional requirements
  - `NFR-###` for non-functional requirements
  - `AC-###` for acceptance criteria
  - `RISK-###` for risk items when needed
- Write user stories as: `As a [role], I want [goal] so that [value]`.
- Map every FR to at least one AC.
- Prefer Gherkin for ACs: `Given / When / Then`.

#### Plan

- Phase work into `MVP`, `Expand`, and `Scale` unless the user gives a different phase model.
- Use vertical slices, not technical layers, when sequencing delivery.
- Define phase gates with measurable criteria.
- Include rollout mechanics early when relevant: feature flags, rings, A/B tests, rollback triggers, kill switches.

## Output Contracts

Use the smallest contract that fits the request.

### PRD or feature spec

Include, as relevant:

- executive summary
- audience or persona definition
- problem, goals, and non-goals
- scope and constraints
- user stories
- FRs, NFRs, and ACs
- KPI and guardrail metrics
- phase roadmap and slices
- dependencies, risks, rollout, and ownership
- assumptions and open questions

### MVP scoping or prioritization

Return:

- product goal
- target user
- P0, P1, P2 feature list
- what is explicitly out of scope
- why the MVP is the smallest proof
- what signal would justify the next phase

### Office-hours diagnostic

Return:

- the specific user or buyer, not a broad category
- the current status quo and why it is painful enough to replace
- the narrowest paid or publicly useful wedge
- the strongest evidence type: `seen it`, `heard it`, `hunch`, or `guess`
- what the user observed that contradicted an assumption
- future-fit: why the market or tooling gets better for this idea
- one recommended next build or validation step

### Delivery governance pack

Return only the requested planning controls, such as:

- KPI and event plan
- rollout rings and rollback conditions
- RACI or stakeholder map
- risk matrix or FMEA-style table
- traceability matrix
- API contract summary
- observability and alert requirements

### Change packet

Use this when the work is larger than a chat answer but smaller than a formal PRD:

- proposal: what changes and why now
- scope: in, out, assumptions, and constraints
- scenarios: user/business flows or requirement cases
- design notes: architecture, UX, data, API, privacy, or rollout decisions that affect implementation
- tasks: ordered build, test, docs, and release steps
- verification: checks, acceptance criteria, rollback, and signoff evidence
- archive decision: accepted, rejected, superseded, shipped, or deferred, with the reason

When creating local files, prefer:

```bash
python3 ${PLUGIN_ROOT}/libraries/prd-strategist/scripts/create_change_packet.py \
  "<change name>" --output-root ./changes --capability "<capability-name>"
```

Use `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1` for any reviewed OpenSpec CLI
inspection. Do not run OpenSpec write/update/dashboard commands unless the user
explicitly asks for that exact lane.

### Exploration note

Use this before committing to a change when the answer depends on discovery:

- question: what needs to be understood
- evidence checked: files, sources, metrics, screenshots, or docs
- options: viable approaches and their tradeoffs
- decision trigger: what would make one option clearly better
- recommended next action: propose, implement, defer, spike, or stop

Exploration should lead to a decision or stop condition. Do not turn it into an
open-ended research lane.

## Reference Files

Load only what the task needs:

- `references/workflow-and-artifacts.md`
  - Write -> Task -> Plan method, discovery flow, IDs, acceptance criteria, KPI guidance, rollout expectations, and artifact contracts
- `references/prd-template-guide.md`
  - section order, editorial structure, document patterns, and guidance for formal deliverables
- `references/feature-table-patterns.md`
  - reusable tables for audiences, prioritization, slices, RACI, traceability, and open questions
- `references/openspec-vibe-adoption.md`
  - OpenSpec-inspired local change-packet workflow, runtime security boundary,
    Vibe Check discovery, opportunity scoring, beginner plan, and checkup mode

When a formal document is requested, read the relevant references here, then use `$doc` to create or polish the `.docx`.

## Defaults

- Default audience: mixed business, design, and engineering readers.
- Default voice: decisive, user-centered, and concise.
- Default phase model: `MVP -> Expand -> Scale`.
- Default priority scale: `P0`, `P1`, `P2`.
- Default requirement rule: every requirement should be testable or explicitly marked as an assumption.
- Default close: end with assumptions, open questions, and the next decision or build step.
