---
name: portfolio
description: Build, edit, target, audit, and sharpen portfolio case studies, contractor-facing case cards, competency evidence maps, service proof inventories, artifact captions, confidentiality checks, reviewer simulations, visitor-journey audits, portfolio playtest plans, and reader-aware proof structures.
---

# Portfolio Crafter

Portfolio Crafter helps a host AI turn real project material into clear,
truthful, reader-aware portfolio case studies. Use it for full case studies,
targeted rewrites, case cards, contractor-facing proof cards, artifact captions,
portfolio audits, confidentiality review, metric-safe impact language, service
proof inventories, competency evidence maps, reviewer simulations, and
interview or deck story continuity. It can also apply game-design transfer
lenses to portfolio and interactive artifacts: visitor core loop, trust
feedback, evidence pacing, optional interaction, accessibility, and anti-gimmick
review.

This skill is public-facing and generic. It must not rely on a private profile, private source register, local file path, personal career history, hidden application packet, or unpublished project evidence.
Its documented package routes are Codex and Claude Code; native installation and first-use support depend on the host and are reported in the [host table](../../README.md#optional-complete-methods-and-runtimes).

## Use This Skill When

- The user wants to build a portfolio case study from raw project notes, artifacts, screenshots, research summaries, or a rough draft.
- The user wants to convert a rough project into a one-page case card.
- The user wants to map portfolio evidence to competencies, reviewer
  questions, or an assessment rubric.
- The user wants to rewrite a generic case-study opening into a role-relevant thesis.
- The user wants artifact captions from supplied facts.
- The user wants portfolio screenshots, proof images, case-card media,
  generated visuals, public-facing imagery, or artifact placement planned or
  audited; use `ux-design-toolkit:design-studio` only when actually discovered; otherwise inspect the real assets with the first-party proof and visual-anchor methods.
- The user wants to target an existing case study to a role, reader, or portfolio format.
- The user wants to translate portfolio material into contractor, consulting,
  service-business, or client-facing proof.
- The user wants to turn a shipped project or case into public proof assets,
  launch notes, social proof campaigns, release announcements, or post-ready
  case snippets.
- The user explicitly asks for website proof planning, buyer path review, or
  portfolio-to-contractor-site structure.
- The user wants to audit a case study for generic language, unclear ownership, missing proof, weak outcomes, or confidentiality risk.
- The user asks how to handle missing, uncertain, sensitive, or unsupported metrics.
- The user needs a case to connect to interview or deck talking points.
- The user wants a scaffolded portfolio practice path, reviewer simulation, or
  support for no metrics, confidential work, group projects, student projects,
  career transition, research-heavy work, visual design-heavy work, or
  technical communication portfolios.
- The user wants to audit a portfolio, case study, or explicit portfolio-site
  plan as a visitor journey, core loop of trust, or playtestable experience.

## Coordination

The following sibling owners are optional. Use a named skill only when it is actually discovered and relevant; otherwise complete this skill's first-party portfolio method without claiming that sibling's review.

- Use `social-content-studio` when portfolio proof needs channel-specific
  posts, hooks, release copy, profile updates, social proof trackers, or
  outreach drafts.
- Use `marketing-strategy-operator` when portfolio proof needs a campaign
  brief, public proof strategy, launch plan, buyer path, offer positioning, or
  measurement plan before social posts or Shareables handoff.
- Use `html-presentation-builder` when a case should become a browser-native
  deck, visual explainer, or progressive-disclosure Shareable.
- Use `learning-experience-designer` when a portfolio artifact should double
  as a teaching asset, workshop, lesson, or course proof object.

## First Move

Identify the task type before writing:

1. Full portfolio case-study build
2. Targeted case-study rewrite
3. Case-card creation
4. Artifact caption writing
5. Portfolio or case audit
6. Confidentiality and redaction review
7. Metrics and unsupported-claim review
8. Interview or deck story continuity from a case
9. Contractor-facing case card or service proof inventory
10. Website proof or buyer path planning, only when explicitly requested
11. Competency evidence map or reviewer simulation
12. Visitor core-loop audit, portfolio playtest, or interaction/gamification review
13. Scaffolded practice or special-context support path
14. Public proof campaign, release note, or social proof asset map

If the user provided enough material, proceed. If a missing fact would change the output materially, ask for that fact or mark it as `[MISSING INFO: ...]`.

## Core Rules

- Treat a portfolio as a proof system, not a gallery.
- Treat a portfolio as an assessment artifact: it helps a reviewer infer
  capability from supplied evidence, artifacts, decisions, constraints, and
  reflection.
- For contractor-facing work, treat the case as buyer risk reduction: what
  problem was unclear, what decision needed evidence, what work was done, what
  changed, and why the user is safe to hire.
- Do not invent projects, employers, institutions, clients, users, team size, dates, tools, research methods, metrics, artifacts, decisions, outcomes, ownership, or permissions.
- Preserve truth while improving focus, structure, hierarchy, and reader fit.
- Start with the target reader and reader speed: 10-second scan, 2-5 minute review, or deep interview review.
- Name the competencies or reviewer questions the case is supposed to answer
  before polishing prose.
- Build case studies around problem, role, constraints, methods, artifacts, decisions, outcomes, and what the case proves.
- Use metrics only when supplied and verified. Otherwise use transparent estimates or non-numeric impact language.
- Mark confidential, private, or sensitive artifacts for redaction before turning them into public copy.
- Keep missing proof visible as `[MISSING INFO: ...]`.
- Separate real proof from generated presentation assets. Screenshots, exports,
  source-backed media, public links, and verified artifacts can support claims;
  generated images, decorative frames, icons, and atmospherics can improve
  comprehension or emotion but must never be positioned as evidence.
- When portfolio visuals combine proof and generated assets, create a small
  source-status map: what is real, what is illustrative, what was edited or
  cropped, what is redacted, and what needs public verification.
- For public proof campaigns, keep the proof object, source link, claim
  boundary, asset order, alt text, and human-review status visible. Do not
  invent engagement, testimonials, client response, or performance metrics.
- Do not build or imply a public website unless the user explicitly asks for website planning.
  When website planning is explicit, plan proof, service fit, reader path, and
  confidentiality before visual design.
- Use game-design transfer lenses to improve visitor journey, evidence
  feedback, progression, emotional pacing, accessibility, and optional
  interaction. Do not use them to invent game-design experience, shipped-game
  claims, playtest findings, metrics, or playful site concepts not requested.
- Keep playful or interactive portfolio layers optional and purposeful. They
  must not block fast access to evidence, resume/contact details, or case
  substance.

- Write for reviewers first: avoid UX/product specialist jargon by default.
  If a term is truly needed, define it in plain language on the same pass.
  For example: `IA` should be written as
  "information architecture (how content is organized)".
- Use a reader-vocabulary baseline, not a craft-vocabulary baseline:
  - Stakeholder decks should use everyday business language
  - Do not assume shared UX, design, or engineering shorthand
  - Every sentence should be understandable by a recruiter, hiring manager,
    contractor, or client without a design glossary.
- Run an abbreviation and insider-term audit before finalizing portfolio copy:
  - Avoid unexplained shorthand such as `IA`, `UI`, `UX`, `viz`, `ATS`, `MCP`,
    `LLM`, and role-specific labels unless the audience clearly expects them.
  - Prefer reader-facing outcomes over craft labels. For example, write
    "made the dashboard easier to scan" before "improved visual hierarchy."
  - Replace low-signal technical phrasing with proof. For example, rewrite
    "AI summary, real data viz, five IA buckets" as
    "automatic summary, clear charts, five screen sections."
  - Ask: "Would a recruiter or stakeholder understand this without a design
    glossary?"

## Recover Visual Proof Before Reconstructing It

When past Stitch, Figma, or design-tool work is available and retrieval is in scope,
look for the original artifact before making a new mockup. Use an installed
library-evidence skill where available. Record authorship support, date or unknown,
version, real role, and what the image directly supports. Account access alone
does not establish authorship, chronology, shipping, or outcomes.

Distinguish an original, an iteration, a new reconstruction/proposal, and a deployed
result. Verify chronology and comparable scope for before/after claims; use
“original / proposed” when that is what the evidence supports. Lead with a result
only when substantiated, then connect action and problem (RAP); otherwise show the
problem, supported action, and actual result or remaining question (PAR). Prefer
one readable screenshot with a decision caption over several paragraphs of process.
AI design consultation is not user research or evidence of measured improvement.

## Visual Readability Rules (for slides, PDFs, case cards, and portfolio web text)

- Body text target: `16px` minimum.
- Subtext target: `14px` minimum, `16px` preferred when format permits
  (especially for important qualifications, outcomes, and risks).
- Never place high-priority claims, outcomes, or proof statements below `16px`.
- For dense slide content, prioritize shortening lines over shrinking type.
- Use clear hierarchy: strong headings, short lines, and generous spacing.
- If output is a slide deck, call out any term that may require local
  definition before finalizing copy.

## Default Workflow

1. Define the target: reader, role, competencies to prove, reviewer decision,
   format, reader speed, and sharing context.
2. Inventory evidence: project facts, artifacts, constraints, methods, decisions, outcomes, metrics, permissions, and unknowns.
3. Choose the case thesis: what this project proves about the candidate's
   judgment, contribution, and role-relevant capability.
4. Draft or revise: structure the case for scanability, proof, buyer or reviewer fit, and defensibility.
5. Audit: check ownership, evidence, metrics, confidentiality, accessibility,
   generic language, unexplained abbreviations, cognitive load, visitor
   journey, interaction usefulness, and transfer to interview/deck/share use.
6. Return next actions: what to verify, redact, source, caption, practice, or
   cut before sharing.

## Output Shapes

Choose the smallest existing shape that fits. Read only its linked template:

| Output | Template |
| --- | --- |
| Full case study | [case-study.md](templates/case-study.md) |
| One-page case card | [case-card.md](templates/case-card.md); make the reader hypothesis explicit |
| Contractor-facing proof card | [contractor-case-card.md](templates/contractor-case-card.md); name the recommendation or decision influenced |
| Artifact captions | [artifact-caption-set.md](templates/artifact-caption-set.md) |
| Case or portfolio audit | [portfolio-quality-rubric.md](references/portfolio-quality-rubric.md); identify the strongest existing material |
| Competency evidence map | [competency-evidence-map.md](templates/competency-evidence-map.md) |
| Visitor core-loop audit | [visitor-core-loop-audit.md](templates/visitor-core-loop-audit.md); recommend the next playtest when relevant |

For other shapes, choose from [the template index](templates/template-index.md).

For a public proof campaign handoff, return:

```markdown
## Public Proof Campaign
- Proof object:
- Target reader:
- Primary claim:
- Source link or artifact:
- Claim boundary:

## Asset Order
| Asset | Purpose | Source status | Alt text | Platform fit |
| --- | --- | --- | --- | --- |

## Copy Hooks
1.
2.
3.

## Human Review
- Verify before posting:
- Do not claim:
- Follow-up tracker:
```

## Reference Navigation

| Need | Read |
| --- | --- |
| Choose the right portfolio workflow and framework | `references/patterns.md` |
| Audit case-study quality | `references/portfolio-quality-rubric.md` |
| Structure a full case study | `references/case-study-structure.md` |
| Turn evidence into a scannable case, bounded PAR/RAP story, or reusable job-specific packet | `references/evidence-to-case.md` |
| Use instructional-design framing for competencies, scaffolds, and reviewer simulation | `references/instructional-design-portfolio.md` |
| Apply game-design transfer to visitor journey, trust loop, playtesting, and anti-gimmick review | `references/game-design-portfolio-transfer.md` |
| Translate portfolio material into buyer-facing contractor proof | `references/contractor-portfolio-strategy.md` |
| Build service proof, contractor case cards, and proof hierarchy | `references/service-proof-and-case-studies.md` |
| Use Knowledge Atlas and File-O-Fun portfolio activities | `references/knowledge-atlas-portfolio-activities.md` |
| Write artifact captions and preserve Figma/video/frame/crop traceability | `references/artifact-captions.md` |
| Handle confidentiality and redaction | `references/confidentiality-and-redaction.md` |
| Handle metrics, evidence, and missing proof | `references/metrics-and-truth.md` |
| Remove generic language | `references/generic-phrase-guardrails.md` |
| Choose a template | `templates/template-index.md` |
| Use optional specialist roles | `agents/agent.md` |

## Agent Roles

Use the agent files as prompt-role guidance when a portfolio task benefits from focused review:

- `agents/portfolio-strategist.md`: reader, format, case selection, and portfolio narrative
- `agents/case-study-writer.md`: full case-study structure and rewrite
- `agents/artifact-caption-editor.md`: captions, alt text, and artifact proof
- `agents/evidence-integrity-reviewer.md`: unsupported claim and metric checks
- `agents/confidentiality-auditor.md`: redaction, sensitivity, and share-readiness
- `agents/buyer-proof-strategist.md`: buyer risk, proof hierarchy, trust path, and case selection
- `agents/service-offer-case-advisor.md`: service-aligned case cards and offer proof
- `agents/portfolio-site-planner.md`: website proof planning only when explicitly requested
- `agents/portfolio-assessment-coach.md`: competency evidence maps, reviewer simulation, scaffolded practice, and special-context support
- `agents/portfolio-transfer-strategist.md`: visitor journey, core loop of trust, interaction usefulness, accessibility, and gimmick risk

## Stop Conditions

A portfolio case is ready for the next human review when:

- The target reader and format are clear.
- The case thesis is specific and role-relevant.
- The competencies or reviewer questions the case should answer are visible.
- The visitor journey and evidence path are clear when the task is portfolio
  site, interactive artifact, or reader-path planning.
- The candidate's contribution is explicit without overstating ownership.
- Every strong claim is supported by supplied evidence.
- Metrics are verified, clearly estimated, or replaced with non-numeric language.
- Artifacts have captions, alt text, and confidentiality notes.
- Missing proof remains visible.
- Generic filler has been replaced with artifacts, decisions, constraints, outcomes, or learning.

For document, PDF, slide, website, visual, and publishing work, use the current [provider boundary](../../references/providers.md) only when that output is requested.

For a UX portfolio case study, use this complete first-party portfolio workflow and its task-matching references. If `uiuxdesigner:ux-portfolio-case-study` is actually discovered, read the full installed provider skill for additional depth. In Codex, install the official `uiuxdesigner@openai-curated-remote` plugin through the native manager and start a fresh task; Claude discovery has not been verified. If absent, report the unavailable provider depth without claiming it was applied. Do not copy its method body or substitute a topical summary. Current user instructions and factual evidence govern all action and claim boundaries.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For the original local portfolio-crafter build, targeted rewrite or audit variant, read and apply the [complete method](references/local-method.original.md) and its task-matching retained support. Keep the current workflow, confirmed evidence and outgoing-writing review in force; preserved method wording does not grant submission or sending authority.
