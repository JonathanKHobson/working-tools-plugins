---
name: campaign
description: "Run a role-specific job application campaign from evidence-backed materials through authorized submission and receipt checks; use for planning, execution, status or first-use help."
---

# Job application campaign

If asked what Career Studio can do or how to start, use the [human guide](../../README.md) to give a short outcome-based menu: role-specific evidence, portfolio proof, interview/outreach preparation, and receipt-checked applications. Invite one concrete role or artifact and identify the evidence needed. For a specified role task, begin the packet or specialist workflow directly; do not repeat onboarding or imply a previous chat established current access.

Finish one role at a time: a tailored packet ready for review, an authorized application with verified submission evidence, or a precisely recorded blocker with one next action. Preserve continuity without turning the private local packet engine into a CRM or auto-apply product.

For authorized job discovery and application batches across job sites, read [job search execution](references/job-search-execution.md): eligibility before selection, requisition deduplication, shared claims/caps/browser ownership, evidence-based answers, role-specific holds, reviewed template reuse, bounded learning and receipt-backed counts. This is part of the campaign workflow, not a duplicate skill. Personal context comes from the [private workspace](../../references/private-workspace.md).

## Start or resume

1. Establish the requested outcome and existing authorization: prepare, submit selected roles, reconcile receipts, or resume. Creating or invoking this skill does not itself authorize sending applications, outreach, publishing portfolios, or changing browser permissions. Reuse authorization already given; do not ask again for routine steps within it.
2. Resolve the actual project and campaign folder. Use the current workspace or the private workspace binding described in [private workspace](../../references/private-workspace.md); verify it exists and read applicable `AGENTS.md`. Locate the requested campaign under `applications/` when that is the workspace layout; verify its current status rather than assuming a previously active campaign remains current or creating a duplicate on resume.
3. Read source records, current handoff, and relevant receipts. Use [campaign-records.md](references/campaign-records.md) for the observed layout and state contract. Reuse existing formats. A dashboard is a derived view, not independent submission proof.
4. Pick the user's specified role, or the highest-priority actionable role using current fit, income, work-mode, and mission constraints. Ask one focused question for a required missing answer while continuing independent preparation. Do not expand into discovery, portfolio redesign, or unrelated coordination unless requested.
5. State the verification path: final files and visual review for preparation; employer acknowledgment or Sent evidence for submission; source-to-tracker agreement for reconciliation. Read [recorded-workflow.md](references/recorded-workflow.md) only for historical provenance or ambiguous recorded states.

## Select and ground the role

- Keep a stable job ID, exact employer/title, requisition/listing identity, application URL, lane, and last-checked date. Deduplicate by canonical listing/requisition before generating or submitting. Distinct requisitions at one employer remain distinct roles. Separate required from preferred qualifications, and label any inferred team problem as an inference rather than a company fact.
- Recheck the official employer listing and live form before acting. Record closed roles and work-mode/location restrictions. Fit and priority scores are assessments, not hiring probabilities.
- Prefer newer reviewed profile evidence and the recipient's reviewed portfolio or evidence bank, when one exists, over old resumes. Preserve source IDs and tiers. Archive, scaffold, and adjacent evidence are not direct support for personal claims; label adjacent support and retain `[MISSING INFO: ...]` in private drafts where needed.
- Never invent metrics, dates, titles, credentials, tools, outcomes, or screening answers. Retrieve authorized connected or local evidence only for a concrete gap or necessary continuity, not as a dependency of every packet.
- If GM/event opportunities are in scope, keep them separate from career roles and retain per-session/event pay. Preserve currency, period, bonus/OTE distinctions, and explicit annualization assumptions. Missing salary or applicant counts remain unknown.

## Prepare the employer-specific packet

1. Reuse `packets/<job-id>/` and inspect finished work. Check whether Job Application Compass is actually installed and exposes the relevant parse, evidence-map, preparation, or validation contracts before calling them. Its private runtime is optional; do not claim its checks ran when unavailable or add MCP features for campaign operations.
2. If that runtime is available, its local generator may provide `generation-brief.md`, `resume.md`, `cover-letter.md`, `evidence-map.md`, `dossier.md`, and `follow-up.md` as drafting scaffolds. Inspect `scripts/prepare_packet.py --help` only when that script exists in the recipient's installed runtime. Otherwise create the needed files in the existing private packet from the posting, reviewed evidence, and this plugin's `resume`, `cover-letter`, and `application-statements` methods; a concise evidence map can pair each claim with its source and any unresolved gap. Make only the files this application needs, and do not call them generator output. Never regenerate scaffolds over finished material. Reuse verified evidence snippets across roles, never a generic master letter or employer-specific praise from another packet.
3. Draft the tailored resume and cover letter from supported evidence, using this plugin's `resume` and `cover-letter` guidance as needed. Use the exact employer/role and remove enthusiasm copied from other companies. Add `application-fields.json` or tailored text responses only as the form requires; use `application-statements` for substantive short answers. Store each screening answer with its question and source/user confirmation: a bare “No” must not migrate to another question.
4. Export role-named PDFs and editable sources as required. Reuse or prepare a deck/tailored portfolio when justified by the role or requested scope; the historical full bundle is not mandatory for every job. Identify required, optional, and not-needed materials.
5. Check names, employer, role, links, dates, claim support, and required answers. Resolve or remove unsupported claims before final export; do not send missing-info markers. Open final PDFs/documents/decks and perform visual QA with 3–8 named anchors recording file/page/region, observation and intended action; recheck changed anchors. Structural validation cannot certify prose or rendering.
6. Record exact final paths/version and readiness. Distinguish local portfolio previews from live employer-accessible URLs. Verify the URL and intended content; never submit localhost links. Publishing requires applicable authorization and privacy review of the actual output. Keep private tracking, raw evidence, and review assets outside the public boundary.

## Complete the application within authorization

1. Reopen the intended employer form. Compare employer, exact role/requisition, packet ID, and filename before each upload. On mismatch, cancel the picker and navigate to the correct packet; do not carry over the previous employer's path.
2. Use an exact absolute path through Go to Folder or the available upload tool. A selected file or clicked Open is only an attempt. Wait for processing and verify the displayed filename beneath each attachment control; inspect errors and parsed fields.
3. Fill questions from the reviewed response record. Record blockers for missing facts, email verification, CAPTCHA, access/login, unavailable upload, required agreement, or closed listing. Use supported user/browser flows for interactive challenges; do not bypass them. Never save verification codes or authentication URLs in campaign records.
4. If final submission lacks authorization, finish independent preparation and make the exact role, materials, answers, and any agreement reviewable before asking. A new NDA/legal agreement or unrelated public release is not silently covered by packet-preparation permission. If submission is already authorized and no new decision is needed, proceed without another generic confirmation.
5. After submitting, observe the result. Confirm employer/requisition and acknowledgment content, not just a generic thank-you tab title. Save a minimal receipt pointer and observation time before navigating away. A click, spinner, disabled button, or attachment list is not a receipt.
6. For email applications, verify the actual Sent item, recipient, subject, and attachments. Record sent separately from employer receipt. Send follow-ups or other outreach only with explicit authorization.
7. If the result is ambiguous, inspect the current page, existing receipts, and narrowly relevant mail first. Keep `attempted-unconfirmed` and a verification next action; do not blindly retry and risk duplication. When the same failure recurs without new evidence, record it and continue an authorized independent step.

## Blockers, receipts, and closeout

- Preserve materials and submission state when blocked. Record issue, scope/job ID, owner, exact action needed, last observation, and independent work. Resolve only after the affected action succeeds or direct evidence shows the issue cleared; retain resolution history.
- Diagnose the current tool's upload path from observed behavior. Change only relevant settings within authorization and verify a real upload afterward; a past setting change is not continuing permission or a universal fix.
- Update source records before refreshing existing dashboard/export tooling when needed for this lane. Do not invent a second tracker. Preserve schema compatibility and unknown fields. A file named “receipt” or assistant-authored status alone cannot prove completion; trace it to actual observed evidence.
- Reconcile counts by distinct job/application identity. Separate prepared, attached, attempted-unconfirmed, sent, and employer-confirmed counts. Sent and confirmed may overlap and must not be added blindly. Exclude outreach and portfolio-publication receipts from application counts.
- Reopen saved records and confirm role, paths, blocker state, receipt source, and totals agree. Visually inspect changed dashboards/exports and recheck anchors before handoff. Report remaining uncertainty.
- After browser automation, close only automation-owned sessions/helpers and verify no automation Chrome session remains or normal visible Chrome is restored without automation-only profile arguments. Follow current project MCP cleanup rules if temporary MCPs were enabled.
- End with completed states, material/receipt links, unresolved blocker and owner, and one next action. Tie totals to evidence and an as-of time. Do not turn unrelated historical actions into tasks or create unsolicited reminders.

## Maintenance

See the plugin [project map](../../docs/project-map.md) for file responsibilities. Validate changes with skill-creator. Review behavior against wrong-employer packets, selected-only attachments, employer receipts, Sent without acknowledgment, stale assistant totals, and unresolved upload/verification blockers. No live application is needed to validate the skill.

For document, PDF, slide, website, visual, and publishing work, use the current [provider boundary](../../references/providers.md) only when that output is requested.

## Full source procedures

Read the complete task-matching bundled procedure through the [native method map](../../library/source-procedures/INDEX.md). The current skill, evidence rules, templates and relevant references own the work directly; a separate letter, prose or UI method plugin is not required. Preserve source facts and apply the final outgoing-writing review before presenting a share-ready artifact.

For targeted job discovery, fit evaluation or a requested skill-gap plan, read only the matching complete method: [discovery and dedup](references/job-discovery-and-dedup.md), [role fit](references/role-fit-evaluation.md), [posting/company research](references/posting-and-company-research.md), [candidate evidence brief](references/candidate-evidence-brief.md) or [evidence-based skill gaps](references/evidence-based-skill-gaps.md). Reuse the existing private tracker and evidence. No regional scraper, Bun installer, personality assessment, automatic sending or new tracking store is added. [Pinned source and disposition](../../libraries/ai-job-search/PROVENANCE.md) preserves full original methods and MIT notice.

## Scoped Atlas reference

For local career concepts, frameworks, activities or source definitions, read [the scoped Atlas library](../../references/atlas-library.md). Use its relevant-only search and full-source selection before adaptation; human browsing and assistant retrieval share the same source records.

When the campaign needs professional visibility or networking, route LinkedIn profiles to resume's [profile method](../resume/references/linkedin-profile.md), individualized messages/inbox decisions to [Career Outreach](../career-outreach/references/linkedin-conversations.md), and reusable stories to [evidence story bank](../../references/evidence-story-bank.md). Social Content owns public post/calendar methods. Do not add a compulsory content campaign to an application request.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Career Strategist, Career Coach, Job Search Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
