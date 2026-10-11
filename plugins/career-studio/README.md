# Career Studio

Version **0.2.1** adds portable MCP discovery through root [`mcp.json`](mcp.json) for the existing optional launchers. Their server identities, runtime bindings and compatibility declarations are preserved; backend availability remains a separate check.

Turn verified career evidence into role-specific resumes, letters, portfolio proof, interview preparation, outreach and application records. A confirmed application requires an employer confirmation page, authenticated submitted status, or matching acknowledgment. A Sent email is separate delivery evidence and does not itself prove employer receipt.

## Start with a real task

| Ask | Bring | You receive |
| --- | --- | --- |
| “Tailor my resume to this job posting using these work examples.” | Posting and real evidence | A role-specific resume with unsupported claims flagged |
| “Build a visual portfolio case from these project artifacts.” | Artifacts, contribution and intended audience | A reviewable case with evidence and status labels |
| “Submit this prepared application and verify the receipt.” | Role packet, live form and authorization | Observed upload/submission state and receipt or precise blocker |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/campaign/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Use the narrow skill for a single resume, letter, case, interview or message. Use campaign for work spanning roles, packets, submissions or receipt reconciliation.

| Task / skill | What it produces |
| --- | --- |
| [application-statements](skills/application-statements/SKILL.md) | Draft or audit truthful job screening answers, personal statements, motivation letters, and scholarship or program application essays from the applicant's real evidence and the exact prompt. |
| [campaign](skills/campaign/SKILL.md) | Run or resume a tailored job-application campaign, tracking roles, evidence-backed materials, blockers, submission attempts, and employer receipts. |
| [career-interviews](skills/career-interviews/SKILL.md) | Prepare evidence-backed interview answers, portfolio walkthroughs, design-challenge practice or compensation expectations and offer comparisons for a named role and stage. |
| [career-outreach](skills/career-outreach/SKILL.md) | Draft career messages, LinkedIn connection notes and DMs, triage recruiter/opportunity inboxes, and prepare proposals or counteroffers from verified evidence. |
| [cover-letter](skills/cover-letter/SKILL.md) | Build and audit truthful employment cover letters, including faculty, career-change, internal, short-form, localized, and referral contexts; handle related career outreach. |
| [portfolio](skills/portfolio/SKILL.md) | Build, edit, target, audit, and sharpen portfolio case studies, contractor-facing case cards, competency evidence maps, service proof inventories, artifact captions, confidentiality checks, reviewer simulations, visitor-journey audits, portfolio playtest plans, and reader-aware proof structures. |
| [portfolio-package](skills/portfolio-package/SKILL.md) | Assemble or refresh coordinated portfolio websites, resumes, and slide decks from local work samples, with shared evidence and consistent requested role variants, such as UX Design and UX Research. |
| [resume](skills/resume/SKILL.md) | Build and audit evidence-backed resumes, recruiter-readable bullets, ATS-safe structure, and matching LinkedIn profile proof. |
| [submissions](skills/submissions/SKILL.md) | Complete or resume job applications using prepared role-specific packets, verify uploads and form answers, capture submission receipts, and update the existing private campaign dashboard and tracker. |

## Included methods and optional runtimes

All nine Career Studio skill heads, complete task procedures, references, templates and role contracts are included. The [native method map](library/source-procedures/INDEX.md) selects letters, situations, ATS checks, application statements, outreach, general/UX interviews and portfolio work directly from this package. These routes need no separate letter, prose or UI method plugin. Historical publisher bodies remain excluded; source records distinguish the current Studio methods from those procedures.

The optional Career Atlas requires a separately installed Activities Templates Atlas runtime and recipient-owned approved catalog. The fixed-domain [launcher](scripts/atlas_library_mcp.py) is declared in portable [mcp.json](mcp.json) for Codex, with [.mcp.json](.mcp.json) and the Claude plugin manifest retained for compatibility; it requires Python 3 on PATH. Copy the [binding example](examples/runtime-bindings/atlas-library.json) only when needed to `~/.config/studio-tools/atlas-library.json`, replace placeholder paths with your own runtime and data, and do not overwrite an existing binding without review. Missing runtime or data is an access gap, not a zero-result search. The optional Job Application Compass is an operator-owned private runtime documented in [integration guidance](docs/job-compass-integration.md); its 29-tool server and personal defaults are not bundled or publicly installable through this package.

| Capability | Codex | Claude Code |
| --- | --- | --- |
| First-party skills and packaged methods | Prepared for native installation; fresh installed first-use verification is pending | Claude Code manifest and source path are supplied; native installation and first-use remain unverified |
| Letters, prose, interviews and portfolio methods | Bundled native procedures; no additional method installation | Same bundled procedures; host tools still require their own verification |
| Career Atlas launcher | `${PLUGIN_ROOT}` paths and working directory in portable `mcp.json` | `${CLAUDE_PLUGIN_ROOT}` launcher path in `.claude-plugin/plugin.json`; backend execution remains a separate check |

## Availability and recovery

The optional `atlas-career` MCP declaration uses `scripts/atlas_library_mcp.py` and a recipient-owned external index for career methods; it is not required for supplied-evidence drafting. See [Atlas setup and limits](references/atlas-library.md). Confirm the server is exposed and a scoped retrieval succeeds before claiming it is usable. If unavailable, work from authorized supplied evidence and name the missing method lookup.

Career evidence and application records live in the selected private project, not this package. See the [project map](docs/project-map.md), [private workspace boundary](references/private-workspace.md) and [output providers](references/providers.md). Edit canonical source here, validate, and export identical distributable files to the public package; native installation, GitHub publication, and live application state each require separate verification. A draft, uploaded attachment, Sent message and employer receipt are different states.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Source and licensing

The stable package ID is `career-studio`; the display name is Career Studio. First-party code is AGPL-3.0-only; first-party documentation, skills, methods, roles and eligible templates are CC BY-SA 4.0. Retained MIT material keeps its source terms. See [licensing](LICENSING.md), [notices](THIRD_PARTY_NOTICES.md), [attributions](SOURCE-ATTRIBUTIONS.md) and the [project map](docs/project-map.md). Candidate facts, application records, Atlas corpus and provider method bodies are not distributed.
