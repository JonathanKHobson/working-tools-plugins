# Workflow and Artifacts

Use this reference when the user needs deeper planning structure, stronger requirement rigor, or multiple delivery artifacts from one request.

## Write -> Task -> Plan

### Write

Use writing to create alignment before implementation:

- Lead with the one-line pitch.
- State the problem before the feature list.
- Clarify who the work is for and what changes for them.
- Describe why now, not just what.
- Keep the prose short enough for executive scanning but specific enough for delivery teams.

Recommended summary structure:

1. What this is
2. Who it is for
3. What the MVP proves
4. What success looks like

### Task

Convert planning into verifiable work units.

#### ID conventions

- `US-001`: user story
- `FR-001`: functional requirement
- `NFR-001`: non-functional requirement
- `AC-001`: acceptance criterion
- `KPI-001`: KPI or guardrail metric when IDs help traceability
- `RISK-001`: risk item
- `DEC-001`: major planning or product decision

#### Story format

`As a [role], I want [goal] so that [value].`

#### Requirement rules

- Make requirements observable and testable.
- Avoid vague words like `intuitive`, `smart`, `seamless`, or `fast` without a measurable definition.
- Separate user need from implementation choice.
- Call out permissions, validations, dependencies, and failure states when they materially affect delivery.

#### Acceptance criteria rules

Prefer Gherkin:

`Given [context]`
`When [action]`
`Then [observable outcome]`

Use more than one AC when a requirement has different paths, roles, or error conditions.

### Plan

Turn requirements into phased, outcome-based delivery.

#### Default phases

- `MVP`: smallest release that proves value
- `Expand`: fills the highest-leverage experience gaps
- `Scale`: automation, integrations, optimization, and operational maturity

#### Slice rule

A slice must deliver a complete user outcome, not just a backend or UI layer.

Bad slice:

- build schema
- build API
- build UI

Good slice:

- let first-time users create an account and complete the core task end-to-end

## Discovery Question Batching

Ask only the questions that materially change the plan. Favor batches of 3-5.

### Batch 1: framing

- What is the product or feature called?
- What is the one-line pitch?
- Who is the primary user?
- What problem is urgent enough to solve now?

### Batch 2: scope

- What must be in scope for the first release?
- What should stay out of scope?
- What constraints matter most: budget, time, staffing, technical debt, or compliance?
- Which platform or surface matters: web, mobile, API, internal tool?

### Batch 3: success

- What business outcome matters?
- What user outcome matters?
- What KPI or guardrail will prove the release worked?
- What would make this not worth building further?

## KPI and Guardrail Guidance

Pick a small, coherent metric set.

### KPI types

- Leading indicators: activation, setup completion, feature adoption, repeat usage
- Lagging indicators: retention, conversion, revenue, churn, NPS
- Guardrails: error rate, support burden, latency, abandonment, operational cost

### Rule of thumb

- Choose 1 north-star outcome metric.
- Choose 2-4 supporting metrics.
- Choose 2-3 guardrails.

## Rollout and Risk Expectations

Include rollout planning when the feature affects revenue, data, core workflows, or operational risk.

Cover:

- flag or no flag
- rollout rings: internal, beta, broad release
- rollback trigger
- kill switch owner
- user or data remediation if something breaks

Use a simple FMEA-style risk record when needed:

- ID
- description
- likelihood 1-5
- impact 1-5
- score
- mitigation
- owner
- watch metric

## Artifact Contracts

Use these as defaults unless the user asks for a different format.

### One-pager

- one-line pitch
- problem
- target user
- proposed solution
- MVP scope
- success metrics
- biggest risk

### Full PRD

- summary
- background
- audience
- goals and non-goals
- scope
- requirements
- metrics
- roadmap
- rollout
- risks
- ownership
- assumptions and open questions

### Ticket-ready breakdown

Group by slice or theme. Each item should include:

- title
- story or requirement ID
- description
- acceptance criteria
- dependencies
- phase
- priority

### Traceability matrix

Each requirement should answer:

- what AC validates it
- what metric proves it worked
- what slice delivers it
- what phase ships it

## When to Use Other Skills

- Use `$ux-writer` when the core task is UI copy, microcopy, error text, CTA wording, or tone.
- Use `$plain-to-dev` when the user mainly needs terminology translation or a brief engineering reframing rather than a broader product plan.
- Use `$doc` when the user wants a polished `.docx` artifact after the planning structure is complete.
