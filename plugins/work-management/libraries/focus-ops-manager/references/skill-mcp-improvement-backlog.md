> Historical source evidence with receiving-host-neutral locators. Listed configuration, availability, old observations and changes are not current facts or instructions for the recipient. Inspect actual callable capabilities and preserve active jobs before acting. No private config or corpus is supplied.

# Skill And MCP Improvement Backlog

Last refreshed: 2026-06-19, Round 10

This backlog captures reusable patterns from public `ai-skills` repositories
and related skill/MCP sources without installing, cloning, enabling, or copying
external code. It is a parking lot for small local improvements to Jonathan's
Codex skills and MCP protocols.

Local inventory checked this pass:

- `~/.codex/skills`: 46 first-party `SKILL.md` files
  remain in the Round 4 catalog scope and in the current raw inventory command.
- First-pass implementation target: `focus-ops-manager` reference rules, not a new
  skill or MCP.
- Round 3 implementation target: `local-data-mcp-builder` external skill/MCP
  intake rule, not a new skill, script, eval harness, or MCP config change.
- Round 4 implementation target: seed provenance catalog for the 46
  first-party Codex skills, not a new runtime registry, eval harness, script,
  MCP config, or `AGENTS.md` change.
- Round 5 implementation target: `focus-ops-manager` front-loaded action rules,
  not a broad rewrite of the skill.
- Round 6 implementation target: `skill-mcp-orchestration.md`
  skill/agent/persona boundary, not new agent or persona files.
- Round 7 implementation target: `codex-operating-protocols.md` phase
  handoff protocol, not a new planning artifact.
- Round 8 implementation target: a compact Codex design harness in
  `frontend-ux`, plus rendered critique routing through `playwright` and
  `design-taste-gate`; not a new skill, AGENTS.md rewrite, eval harness,
  script, MCP config, external clone, or install.
- Round 9 implementation target: a reproducible harvest map for 12 public
  skill/workflow repos, plus small edits to existing planning, translation,
  design, project-structure, and JAC guidance; not a new skill, external clone,
  external install, runtime import, browser automation, or MCP baseline change.
- Round 10 implementation target: integrate `kunchenguid/lavish-axi` as a
  guarded local skill plus Shareables build-time review-loop guidance; not an
  external install, global hook, browser automation run, or canonical pipeline
  dependency.
- First-pass boundary: no edits to `$PROJECT_VOLUME/AGENTS.md`; no external
  repo clone; no install scripts; no MCP baseline changes.

## Pattern Cards

### 1. Rule Tiering

- Source: <https://github.com/ciembor/agent-rules-books>
- Reusable pattern: Keep canonical rules, task-use rules, and tight-context
  fallbacks separate instead of forcing every instruction into one always-on
  file.
- Local target: `codex-operating-protocols.md` and future skill reference
  files.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Add the `External Pattern Harvest` protocol as a compact
  always-available operating rule instead of a large new skill.
- Validation: Run a local search for `External Pattern Harvest` under
  `~/.codex/skills/focus-ops-manager`.

### 2. Skill Quality Dimensions

- Source: <https://github.com/zjunlp/SkillNet>
- Reusable pattern: Review skills against explicit quality dimensions instead
  of judging them by vibe or popularity.
- Local target: Future lightweight skill review checklist.
- Effort: Low
- Impact: Medium
- Risk: Low
- First-pass action: Implemented in Round 2 as
  [skill-review-mini-rubric.md](skill-review-mini-rubric.md), without a full
  eval harness.
- Validation: The mini-rubric covers trigger clarity, action boundary,
  source/provenance, verification, safety/install boundary, context cost, and
  severity buckets.

### 3. Skill Lifecycle Phases

- Source: <https://github.com/AgentSkillOS/SkillAnything>
- Reusable pattern: Use a phased path for new or heavily changed skills:
  analyze -> design -> implement -> test -> benchmark -> optimize -> package.
- Local target: Future new-skill creation protocol or
  `mcp-skill-package-structure.md`.
- Effort: Medium
- Impact: Medium
- Risk: Medium
- First-pass action: Do not reframe existing skills wholesale. Use this only
  when creating a new skill or materially restructuring one.
- Validation: New skill proposals name which phase they are in and do not jump
  to packaging before a trigger test exists.

### 4. Evidence Collectors Plus Verifier

- Source: <https://github.com/Bhanunamikaze/Agentic-SEO-Skill>
- Reusable pattern: Separate evidence collection, LLM analysis, confidence
  labels, prioritization, and verifier/dedupe passes.
- Local target: Research-heavy skills and MCP-backed report workflows.
- Effort: Medium
- Impact: High
- Risk: Medium
- First-pass action: Keep as a candidate for skills that produce reports,
  audits, or public artifacts; do not add scripts during this pass.
- Validation: Future report skills should name evidence, confidence, impact,
  fix, and verifier behavior.

### 5. Provenance-Rich Skill Catalogs

- Source: <https://github.com/wondelai/skills>
- Reusable pattern: List each skill with what it does and what source,
  framework, book, or authority it is based on.
- Local target: Future skill inventory or discovery document.
- Effort: Low
- Impact: Medium
- Risk: Low
- First-pass action: Implemented in Round 4 as
  [skill-provenance-catalog.md](skill-provenance-catalog.md).
- Validation: The catalog distinguishes original local workflow rules,
  platform/API skills, local project craft, maintenance/debugging skills,
  external inspiration, deprecated compatibility, and uncertain provenance.

### 6. MCP/CLI Boundary And Deterministic Checks

- Source: <https://github.com/m0n0x41d/haft>
- Reusable pattern: Keep reasoning surfaces, runtime commands, and deterministic
  checks distinct; use local check commands for structural guarantees.
- Local target: MCP debugging and local data MCP builder references.
- Effort: Medium
- Impact: High
- Risk: Medium
- First-pass action: Backlog for MCP reliability work; do not change live MCP
  commands or configs in this pass.
- Validation: Future MCP improvements should identify whether they changed
  launcher/config, routing contract, schema validator, retrieval budget, or
  package shape.

### 7. Simple Agent Architecture First

- Source: <https://github.com/iusztinpaul/designing-real-world-ai-agents-workshop>
- Reusable pattern: Prefer one capable agent with specialized tools before
  splitting work into many agents; use eval/review loops where reliability
  matters.
- Local target: Agent orchestration guidance and future MCP/skill design.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Fold into the harvest protocol as a bias toward one local
  patch before new agents, skills, or MCPs.
- Validation: Future agent proposals should explain why one agent plus tools is
  insufficient before adding more agents.

### 8. Real Expertise Over Generic Advice

- Source: <https://agentskills.io/skill-creation/best-practices>
- Reusable pattern: Skills should be grounded in shipped local work, runbooks,
  corrections, project artifacts, and real failure cases, not generic AI-written
  best practices.
- Local target: Future skill edits and new-skill proposals.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Captured in the mini-rubric as source/provenance and
  "would the agent get this wrong without the skill?" checks.
- Validation: A skill review should name whether the skill came from local
  execution, external inspiration, or a generic draft.

### 9. Trigger Eval Pairs

- Source: <https://agentskills.io/skill-creation/optimizing-descriptions>
- Reusable pattern: Test descriptions with should-trigger and
  should-not-trigger prompts so activation is not judged by intuition alone.
- Local target: Skill frontmatter descriptions.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Captured in the mini-rubric as the two should-trigger and
  two should-not-trigger prompt check.
- Validation: Any skill description cleanup should include at least two
  positive and two negative example prompts before broadening triggers.

### 10. With/Without Skill Comparison

- Source: <https://agentskills.io/skill-creation/evaluating-skills>
- Reusable pattern: Compare agent output with the skill enabled versus without
  it before assuming the skill adds value.
- Local target: Future evals for repeatable transformation or routing skills.
- Effort: Medium
- Impact: Medium
- Risk: Medium
- First-pass action: Keep as backlog; Round 2 intentionally stops at a manual
  rubric.
- Validation: Only create eval JSON when a skill has repeatable outputs,
  trigger regressions, file writes, or routing behavior worth testing.

### 11. Severity-Triage Before Editing

- Source:
  <https://raw.githubusercontent.com/trailofbits/skills/main/plugins/skill-improver/skills/skill-improver/SKILL.md>
- Reusable pattern: Separate critical, major, minor, and defer findings so
  review does not become polishing.
- Local target: Skill review workflow.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Implemented in the mini-rubric severity section.
- Validation: Minor findings are evaluated for behavior impact before edits.

### 12. Front-Loaded Action Rules

- Source: <https://github.com/iliaal/ai-skills>
- Reusable pattern: Put critical behavioral rules first, keep skills tight,
  favor actions over explanations, and pair every "do not" with a "do instead."
- Local target: Future skill cleanup passes.
- Effort: Low
- Impact: Medium
- Risk: Low
- First-pass action: Implemented in Round 5 with a compact
  `Front-Loaded Action Rules` section in `../SKILL.md`.
- Validation: `focus-ops-manager` now names the deliverable-first, displacement,
  80% shipping, and context-cost rules before the longer workflow.

### 13. Source-Derived Progressive Disclosure

- Source: <https://reaviz.dev/docs/skills>
- Reusable pattern: Keep core skill instructions small and load detailed
  source-derived references only when the task needs them.
- Local target: Large or multi-reference local skills.
- Effort: Medium
- Impact: Medium
- Risk: Low
- First-pass action: Captured in the mini-rubric context-cost section.
- Validation: A skill review should flag reference files that load by habit
  instead of by task trigger.

### 14. Skill/Agent/Persona Separation

- Source: <https://github.com/alirezarezvani/claude-skills> and
  <https://github.com/alirezarezvani/claude-skills/blob/main/orchestration/ORCHESTRATION.md>
- Reusable pattern: Separate skills as "how to execute," agents as scoped task
  workers, and personas as judgment or voice layers.
- Local target: Future skill/MCP package design and `focus-ops-manager` routing.
- Effort: Low
- Impact: Medium
- Risk: Low
- First-pass action: Implemented in Round 6 as a
  `Skill / Agent / Persona Boundary` section in
  [skill-mcp-orchestration.md](skill-mcp-orchestration.md).
- Validation: Future proposals should name whether the local artifact is a
  skill, agent, persona, reference, or MCP runtime, and default to tightening
  an existing surface first.

### 15. Cross-Agent Portability Boundary

- Source: <https://github.com/alirezarezvani/claude-skills>
- Reusable pattern: Treat cross-agent conversion as packaging and distribution
  work, not as a reason to widen the local Codex baseline during discovery.
- Local target: `local-data-mcp-builder` external skill/MCP intake guidance.
- Effort: Low
- Impact: High
- Risk: Medium
- First-pass action: Implemented in Round 3 as the
  `External Skill/MCP Intake` note in
  `../local-data-mcp-builder/SKILL.md`.
- Validation: `local-data-mcp-builder` now says external repos stay
  inspect-only during harvest and any copying, adapting, installing, running,
  converting, packaging, or wiring routes through `personal-security-check`.

### 16. stdlib-only Helper Scripts

- Source:
  <https://github.com/alirezarezvani/claude-skills/blob/main/SKILL-AUTHORING-STANDARD.md>
- Reusable pattern: When executable helpers are justified, prefer narrow
  stdlib-only CLI scripts with structured output, sample data, and one clear
  job.
- Local target: Future MCP/skill package helpers and
  `mcp-skill-package-structure.md`.
- Effort: Medium
- Impact: Medium
- Risk: Low
- First-pass action: Backlog only. Do not add scripts until a specific local
  workflow needs repeatable validation or generation.
- Validation: A future script proposal should explain why Markdown guidance is
  insufficient, how the helper runs without new dependencies, and what output
  shape proves success.

### 17. Skill Security Threat Surfaces

- Source:
  <https://github.com/alirezarezvani/claude-skills/blob/main/engineering/skill-security-auditor/SKILL.md>
- Reusable pattern: External skill review should explicitly check code
  execution, prompt injection, dependency, filesystem, credential, and
  exfiltration surfaces before any adaptation or install.
- Local target: `personal-security-check` routing from
  `local-data-mcp-builder`.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Captured in Round 3 by expanding `local-data-mcp-builder`
  intake language to require security review before external code movement.
- Validation: Future external code paths should not skip
  `personal-security-check`, even when the action is "just adapt this" rather
  than "install this."

### 18. Phase Handoff Summaries

- Source:
  <https://github.com/alirezarezvani/claude-skills/blob/main/orchestration/ORCHESTRATION.md>
- Reusable pattern: Use phase handoff summaries when a workflow switches
  phases: carry forward decisions, artifacts, and open items so the next phase
  does not restart from unclear context.
- Local target: `focus-ops-manager` Ship Log behavior and future multi-skill
  workflows.
- Effort: Low
- Impact: Medium
- Risk: Low
- First-pass action: Implemented in Round 7 as a `Phase Handoff` protocol in
  [codex-operating-protocols.md](codex-operating-protocols.md).
- Validation: Future multi-stage skill/MCP work can close each phase with
  phase, decision, artifacts, verification, next phase, stop condition, and
  what not to touch.

### 19. Quality-Tier Gates

- Source:
  <https://github.com/alirezarezvani/claude-skills/blob/main/SKILL_PIPELINE.md>
- Reusable pattern: Use explicit quality tiers and merge gates for new or
  high-risk skills, while keeping small language patches on the lighter
  mini-rubric path.
- Local target: Future new-skill lifecycle guidance and
  `skill-review-mini-rubric.md`.
- Effort: Medium
- Impact: Medium
- Risk: Medium
- First-pass action: Backlog only. Round 3 does not create a full eval harness
  or quality scoring system.
- Validation: New skill proposals should state whether they need only the
  mini-rubric, trigger pairs, with/without comparison, or a full eval gate.

### 20. Rendered Design Harness

- Source:
  <https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4>,
  <https://developers.openai.com/codex/skills>,
  <https://www.anthropic.com/engineering/harness-design-long-running-apps>,
  <https://www.anthropic.com/news/claude-design-anthropic-labs>,
  <https://github.com/topics/ai-skills>, and
  <https://github.com/alirezarezvani/claude-skills>
- Reusable pattern: Make subjective frontend quality more reliable by
  front-loading art direction, design-system constraints, realistic content,
  rendered browser inspection, skeptical critique, and focused polish passes.
- Local target: `frontend-ux`, `design-taste-gate`, and
  `skill-mcp-orchestration.md`.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Implemented in Round 8 with
  `frontend-ux/references/codex-design-harness.md` (owned by the separate frontend skill),
  a `frontend-ux` trigger for visually important work, a rendered-evidence
  note in `design-taste-gate`, and an orchestration chain through Playwright.
- Validation: Future visually important UI work should name a visual thesis,
  content thesis, surface register, dominant idea, design-system inventory,
  token plan, generic-risk list, rendered QA path, and polish passes before
  final signoff.

### 21. Spec Artifact Lifecycle

- Source: <https://github.com/Fission-AI/OpenSpec>
- Reusable pattern: For implementation-affecting changes, keep a small lifecycle
  of proposal, requirements/specs, design notes, tasks, verification, and
  archive/decision rather than relying on chat history alone.
- Local target: `prd-strategist` and `project-structure-architect`.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Added lightweight change-packet guidance to
  `prd-strategist` and codebase-map/onboarding guidance to
  `project-structure-architect`; do not install or run OpenSpec.
- Validation: Future planning work can produce a small change packet without
  adding a new CLI, daemon, or formal spec repo.

### 22. Beginner Build Translation And Checkup

- Source: <https://github.com/TexasBedouin/vibe-check>
- Reusable pattern: A non-coder-friendly build helper should translate the idea
  into problem, user, outcome, rules, done criteria, and the next concrete file
  or command, with a checkup mode for existing AI-built projects.
- Local target: `plain-to-dev`, `prd-strategist`, and `focus-ops-manager`.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Added a beginner build translation/checkup mode to
  `plain-to-dev`; do not create a separate vibe-check skill unless repeated use
  proves that `plain-to-dev` and `prd-strategist` cannot cover it.
- Validation: Future beginner app ideas should produce an implementation-ready
  shape without jargon or a second planning system.

### 23. Design Control Dials

- Source: <https://github.com/Leonxlnx/taste-skill> and
  <https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>
- Reusable pattern: Before polishing visuals, explicitly set a few dials such
  as variance, motion, density, register, and reference source so "make it less
  generic" turns into concrete visual decisions.
- Local target: `design-taste-gate`, `frontend-ux`, and future Shareables
  design-system notes.
- Effort: Low
- Impact: High
- Risk: Low
- First-pass action: Added design-control dials to `design-taste-gate` and the
  frontend design harness.
- Validation: Future UI critique should say which dial moved and why, not just
  label the output generic.

### 24. Codebase Map Before Interactive Graph

- Source: <https://github.com/Egonex-AI/Understand-Anything>
- Reusable pattern: Codebase understanding benefits from explicit entrypoints,
  domain terms, data flows, and dependency risks before an interactive
  knowledge-graph/runtime is justified.
- Local target: `project-structure-architect`, `local-data-mcp-builder`, and
  Shareables workflow notes.
- Effort: Low now, Medium if a runtime graph is later approved
- Impact: Medium
- Risk: Medium
- First-pass action: Added a static codebase-map/onboarding default to
  `project-structure-architect`; defer runtime graph/dashboard imports pending
  security review.
- Validation: Before any graph UI or MCP import, a static `docs/project-map.md`
  should name the missing insight the runtime would add.

### 25. Current Social Sentiment Research

- Source: <https://github.com/mvanhorn/last30days-skill>
- Reusable pattern: Time-bounded social/current-web research should separate
  source list, recency window, confidence, prompt-injection risk, and output
  contract.
- Local target: Future research/reporting skill or MCP workflow, not a current
  install.
- Effort: Medium
- Impact: Medium
- Risk: High
- First-pass action: Backlog only. Do not copy scripts, run MCPs, or add API
  dependencies until a security and source-quality review is complete.
- Validation: A future adoption pass must identify exact sources, credentials,
  rate limits, injection handling, and why existing web/research flows are
  insufficient.

### 26. Career Ops As Usefulness Test, Not CRM Expansion

- Source: <https://github.com/santifer/career-ops>
- Reusable pattern: Job-search workflows benefit from modes and routing, but
  the local Job Application Compass should judge them by real packet usefulness,
  not by adding CRM, auto-apply, scraping, or autonomous sending behavior.
- Local target: Job Application Compass planning docs.
- Effort: Low
- Impact: Medium
- Risk: Medium
- First-pass action: Added a career-ops comparison note to the JAC skill
  extraction loop and kept it inside the existing `JAC-SF-010` usefulness check.
- Validation: After 2-3 real application packets, retire any ceremony that does
  not improve claim integrity, submission readiness, or first usable drafts.

### 27. Engineering Lifecycle Patterns

- Source: <https://github.com/obra/superpowers>,
  <https://github.com/anthropics/skills>,
  <https://github.com/mattpocock/skills>,
  <https://github.com/garrytan/gstack>, and
  <https://github.com/addyosmani/agent-skills>
- Reusable pattern: The best recurring signal across engineering skill repos is
  not another generic skill; it is source-grounded work, incremental changes,
  explicit verification, skeptical review, and clear stop conditions.
- Local target: Existing `focus-ops-manager`, GitHub, planning, debugging, and
  frontend skills.
- Effort: Low for guidance, High for future evals
- Impact: High
- Risk: Low
- First-pass action: Captured as Round 9 synthesis in this backlog; no duplicate
  engineering workflow skill was created.
- Validation: Future harvest rounds should update the smallest existing skill
  that owns the behavior, or leave the pattern in this backlog.

### 28. Local Artifact Review Loop

- Source: <https://github.com/kunchenguid/lavish-axi>
- Reusable pattern: HTML artifacts benefit from a local review loop where a
  render-time layout gate catches machine-readable faults before human review,
  the reviewer annotates rendered elements/text, and the agent polls those
  notes back into the next fix.
- Local target: New `lavish-axi` wrapper skill and Shareables build-time review
  guidance.
- Effort: Low for guidance, Medium for a native overlay or MCP callable tool.
- Impact: High for visual artifacts and single-file Shareables.
- Risk: Medium because the external runtime uses `npx`, a local server,
  browser sessions, hooks, dependencies, and optional CDN design fallbacks.
- First-pass action: Created a local `lavish-axi` skill and Shareables guidance
  that borrows the layout-gate/annotation/poll pattern while requiring sandbox,
  safety review, and exported-artifact portability. Do not run or install the
  external CLI by default.
- Validation: A future pilot must prove one real annotation loop, fixed layout
  warnings, no shipped SDK/overlay/CDN/localhost/private paths, and a clear
  keep-side-tool vs rebuild-native decision.

## Prioritization

| Rank | Pattern | Effort | Impact | Status |
| --- | --- | --- | --- | --- |
| 1 | Rule Tiering | Low | High | Implemented in first pass |
| 2 | Simple Agent Architecture First | Low | High | Captured as protocol bias |
| 3 | Skill Quality Dimensions | Low | Medium | Implemented in Round 2 |
| 4 | Trigger Eval Pairs | Low | High | Captured in Round 2 rubric |
| 5 | Severity-Triage Before Editing | Low | High | Implemented in Round 2 |
| 6 | Real Expertise Over Generic Advice | Low | High | Captured in Round 2 rubric |
| 7 | Cross-Agent Portability Boundary | Low | High | Implemented in Round 3 |
| 8 | Skill Security Threat Surfaces | Low | High | Captured in Round 3 intake rule |
| 9 | Provenance-Rich Skill Catalogs | Low | Medium | Implemented in Round 4 |
| 10 | Front-Loaded Action Rules | Low | Medium | Implemented in Round 5 |
| 11 | Skill/Agent/Persona Separation | Low | Medium | Implemented in Round 6 |
| 12 | Phase Handoff Summaries | Low | Medium | Implemented in Round 7 |
| 13 | Evidence Collectors Plus Verifier | Medium | High | Next candidate |
| 14 | MCP/CLI Boundary And Deterministic Checks | Medium | High | Backlog |
| 15 | stdlib-only Helper Scripts | Medium | Medium | Backlog |
| 16 | Skill Lifecycle Phases | Medium | Medium | Backlog |
| 17 | Source-Derived Progressive Disclosure | Medium | Medium | Backlog |
| 18 | With/Without Skill Comparison | Medium | Medium | Backlog |
| 19 | Quality-Tier Gates | Medium | Medium | Backlog |
| 20 | Rendered Design Harness | Low | High | Implemented in Round 8 |
| 21 | Spec Artifact Lifecycle | Low | High | Implemented in Round 9 |
| 22 | Beginner Build Translation And Checkup | Low | High | Implemented in Round 9 |
| 23 | Design Control Dials | Low | High | Implemented in Round 9 |
| 24 | Codebase Map Before Interactive Graph | Low | Medium | Implemented in Round 9 |
| 25 | Current Social Sentiment Research | Medium | Medium | Security-review backlog |
| 26 | Career Ops As Usefulness Test, Not CRM Expansion | Low | Medium | Routed to JAC-SF-010 |
| 27 | Engineering Lifecycle Patterns | Low | High | Captured as synthesis |
| 28 | Local Artifact Review Loop | Low | High | Implemented in Round 10 |

## Round 2 Implemented Improvement

Created [skill-review-mini-rubric.md](skill-review-mini-rubric.md) for manual
review of existing skills. It covers trigger clarity, action boundary,
source/provenance, verification, safety/install boundary, context cost, and
severity buckets. It explicitly blocks automatic polishing of minor issues.

## Round 3 Implemented Improvement

Reviewed `local-data-mcp-builder` with the mini-rubric and fixed the main
major-but-small gap: external skill/MCP inspiration was routed to security
review, but not explicitly through the harvest, backlog, and rubric loop first.
Added an `External Skill/MCP Intake` section to
`../local-data-mcp-builder/SKILL.md` so future external skill or MCP ideas stay
inspect-only during harvest and route through `personal-security-check` before
any copying, adapting, installing, running, converting, packaging, or wiring.

## Round 4 Implemented Improvement

Created [skill-provenance-catalog.md](skill-provenance-catalog.md) as a seed
routing and provenance reference for the 46 first-party Codex skills. It is not
an authoritative runtime registry. It classifies each skill by dominant
provenance signal and marks unclear origins as `needs-review` instead of
inventing source history.

## Round 5 Implemented Improvement

Applied the mini-rubric to the high-use `focus-ops-manager` skill and fixed the
major-but-small gap that the highest-value behavior rules were present but not
front-loaded. Added `Front-Loaded Action Rules` to keep broad or scattered work
anchored to one deliverable, one displacement decision, and an 80% shipping
threshold before extra scaffolding.

## Round 6 Implemented Improvement

Added `Skill / Agent / Persona Boundary` to
[skill-mcp-orchestration.md](skill-mcp-orchestration.md). This keeps future
skill/MCP inspiration from turning automatically into new agents, personas, or
runtime surfaces when a small skill or reference edit would do.

## Round 7 Implemented Improvement

Added `Phase Handoff` to
[codex-operating-protocols.md](codex-operating-protocols.md) so multi-round
skill/MCP work can pass forward decisions, artifacts, verification, next phase,
stop condition, and what not to touch without creating a heavier planning
system.

## Round 8 Implemented Improvement

Created
`frontend-ux/references/codex-design-harness.md` (owned by the separate frontend skill)
as a load-on-demand frontend design harness for polished first-pass UI and
visual artifacts. Updated `frontend-ux` to require the harness for visually
important work, updated `design-taste-gate` to prefer rendered evidence when
code or artifacts exist, and added the orchestration route:
`frontend-ux` -> `playwright`/`playwright-interactive` -> `design-taste-gate`.
Use `communication-story-crafter` in that chain when narrative, portfolio
framing, stakeholder trust, or public-facing proof affects the artifact.

## Round 9 Implemented Improvement

Created a reproducible harvest package under
`~/Documents/Codex/2026-06-18/can-we-use-these-skills-on/work/skill-harvest`
and a user-facing map under
`~/Documents/Codex/2026-06-18/can-we-use-these-skills-on/outputs/skill-harvest`.
The pass inspected 478 local/plugin skill files and 188 external skill items
across 12 public repos using local reads plus GitHub API/raw reads only.

Applied the first safe local update pass by tightening existing skills instead
of importing new ones:

- `prd-strategist`: lightweight change packets inspired by OpenSpec.
- `plain-to-dev`: beginner build translation/checkup mode inspired by
  vibe-check.
- `design-taste-gate` and `frontend-ux`: design-control dials from taste/UI
  skill patterns.
- `project-structure-architect`: static codebase map before interactive graph
  or runtime import.
- Job Application Compass planning note: career-ops comparison folded into the
  existing real-application usefulness review.

Deferred `last30days`, `Understand Anything` runtime/dashboard behavior, GStack
browser/runtime helpers, and other external executable surfaces until a focused
security review proves a local gap that existing skills and MCPs cannot cover.

## Round 10 Implemented Improvement

Integrated `kunchenguid/lavish-axi` with the same inspect-first treatment:
added it to the harvest scripts, created a local `lavish-axi` wrapper skill,
updated Shareables workflow and quality gates with a build-time review-loop
option, and kept runtime use behind sandbox, explicit approval, and
`personal-security-check`.

The adopted gap is narrow and real: local artifact annotation feedback plus a
rendered layout gate before human review. The external CLI, global hooks,
browser session, local server, and CDN fallback remain non-default. Published
Shareables must still export as static/public-safe artifacts with no annotation
overlay, SDK, `localhost`, private paths, or unapproved runtime dependency.

## Design Harness Follow-Up Backlog

- Design example library: collect a small local set of good/bad screenshots or
  Markdown taste notes after real shipped work, not before.
- Claude-to-Codex design distiller: when Claude produces a strong artifact,
  extract its visual thesis, layout rules, typography rules, color rules,
  spacing rules, component rules, motion rules, and "avoid" list for Codex.
- Trigger pairs for visual-design tasks: add should-trigger and
  should-not-trigger examples for `frontend-ux` and `design-taste-gate` if
  activation becomes noisy.
- With/without harness comparison: run a small comparison only after a real
  repeated frontend task appears; do not create eval JSON during this round.

## Next Candidate

Use `Evidence Collectors Plus Verifier` when a report-producing or
audit-producing skill next needs tightening. Keep it as a
medium-effort/high-impact pass: separate evidence collection, analysis,
prioritization, and verification before adding scripts or eval JSON.


## 2026-09-10: applied internal efficiency pass

- Adopted: concise global policy and three local entrypoints; conditional context reads; one model-routing reference; Luna/medium worker defaults with three spawned-worker ceiling. Sources: https://learn.chatgpt.com/docs/build-skills and https://learn.chatgpt.com/docs/agent-configuration/subagents. Validated skills, routing, parser keys and six independent routing scenarios.
- Adopted: exact-ID plugin settings for five duplicate local bundles and five previously-disabled remote packages. Source: local installed manifest and whole-tree comparisons; caches and source retained. Fresh-session exposure is a separate verification state.
- Adopted: existing prompt hook skips pressure subprocess for simple questions; explicit symptoms and broad work still checked. Twelve self-test cases pass.
- Reuse without install: existing Figma native tools, PyMuPDF rendering/preflight and Playwright screenshots/traces. Sources: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/, https://github.com/pymupdf/PyMuPDF, https://playwright.dev/docs/test-snapshots. No executable upstream code copied.
- Deferred: uv install, creative/TTRPG package ownership migration, large vibe-check split, and external filesystem cleanup. Prefer one proven workflow improvement before another runtime or catalog. Current packaging examples: https://github.com/openai/plugins.
- Report: ~/Documents/Codex/2026-09-10/so-based-on-my-codex-usage/outputs/codex-efficiency-report.md. Private before-state and measurements are retained in that task; never copy credential-bearing config backups into public packages.
- Final owner check found two old packaged policy entrypoints still enabled; selectively excluded those installed paths with `skills.config`, retaining their bundles' unique tools. Refresh these version-specific exclusions after package updates.


## Dashboard and infographic guidance — 2026-09-27

Implemented original, instruction-only support in UX Design Toolkit (`dashboard-design`) and Graphic Design Studio (`infographic-design`), with focused design-studio and offline palette lookup handoffs. Data Analytics and Build Web Data Visualization retain their engines and existing specialist policies. Adopted question-led composition and chart-specific color judgment; corrected accessibility/median-reference conflicts; deferred third-party runtimes, icon search, additional catalogs and renderers. Sources and scoped security evidence live in UX Toolkit's `skills/dashboard-design/references/research-and-security.md`. Validation: skill/plugin checks, local links, routing audit, independent fixture-based forward test and source/cache parity after reinstall. Behavioral/rendered benchmark performance remains untested; no product dashboard was changed or published.


## Writing patterns without duplicate plugins — 2026-09-28

Adopted original, conditional guidance in Writing Quality Studio (technical clarity and evidence-bounded academic review), Creative Writing Studio (preserve intentional ambiguity; prose-first rewrites), and cover-letter-crafter (requirement-to-proof tailoring). Academic Writing Toolkit retains its five existing tools. Sources: marketplace entrypoints for Plain English, Natural Writing, Human Writing, AI Humanizer, Cover Letter Writer and Research Writing Guardrails, inspected through the native plugin reader. Rejected promotional footers, detector/ATS scores, blanket wording quotas and unverified journal house rules. Deferred all six installations: no distinct runtime or skill gap justified them. Detailed sources, decisions and tool-probe limits: `~/Documents/Codex/2026-09-27/ak/outputs/writing-pattern-harvest.md`.



## Studio consolidation — 2026-09-29

Adopted: all 74 inspected writing-source skill bodies mapped to conditional capabilities in Writing Quality, Creative Writing, Research, Career, Marketing Strategy and Social Content studios. Authentic voice remains inside Writing Quality; the narrow UX follow-up entrypoint is retired into general communication. Career owns seven reusable skills; candidate facts, answers, resumes, application ledger and dashboard stay in the external private workspace.

Adopted: all 24 Impeccable command families and eight reference families, one pinned source-built ARM runtime in UX, and an owned project-scoped Codex/Claude hook adapter. Real browser detection plus live accept/discard passed; upstream installer/update/download paths are not used. Graphic Design and Sites hand off to that owner rather than duplicate a detector. UX and Critical Compass use packaged stdio bridges with private external backend bindings; routine Critical Compass metadata is reduced while full contracts remain available deliberately. Job Application Compass remains an optional private packet engine, not bundled personal data.

Adopted: consistent Studio display names while keeping existing plugin IDs, three focused new owners (Career, Marketing Strategy, Social Content), current-social-research in Research, namespaced routing, and native Claude marketplace adapters. Full snapshots and measured receipts live in the Managing My Computer consolidation report. Provider connectors and app authentication remain provider-owned; app UI, public distribution and automated job applications were not part of this release.

## 2026-10-01 — Find Skills integration

Adopt: Vercel find-skills at commit `3694740352eeef5cdd689af694c485f1ff62eec3`, personalized as `work-management:find-skills`. Existing-owner and real-gap checks precede search; Master Security Toolkit source/adaptation review precedes admission. Global npx installation, popularity-based trust and blanket updates were replaced. The complete private ecosystem audit and verification receipts are in Managing My Computer `work/find-skills-2026-10-01/`. Other candidate expansions remain recommendations until scoped implementation. No new runtime or scheduled installer.

## 2026-10-06 — Widget research integrated

Adopted source-linked generic embedded-widget UX in UX Design Studio, MCP technical boundaries/test plan in maintained personal Build MCP Apps, and analytical-state guidance in Data Visualization Toolkit. Complete Alpic 1.0.1 methods/license preserved; remote duplicate retired after native local install and byte parity. Deferred framework/runtime imports lacking a concrete product need and exact dependency/license review. Research, archive/security scan, eight scenario reasoning review, no-blocking routing audit and installation evidence: `~/Documents/ChatGPT/Managing My Computer/work/library-widgets-2026-10-06/research/integration-review.md`. No actual-host compatibility or user-study claim; no runtime changes in this pass.
