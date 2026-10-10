---
name: submissions
description: Complete or resume job applications using prepared role-specific packets, verify uploads and form answers, capture submission receipts, and update the existing private campaign dashboard and tracker. Use for submission execution or reconciliation, not job sourcing or portfolio rebuilding.
---

# Job application submissions

Close one application loop: match packet → complete form → submit within authorization → capture evidence → save and verify tracking. Finish the current employer before moving to another unless blocked or the user redirects.

For private workspace resolution, ledger fields, builder, and receipt checks, read [references/compass-workflow.md](references/compass-workflow.md). Historical examples establish workflow lessons, not current application status, personal facts, or authorization. Computer History is optional for ordinary execution; use it when asked to reconstruct prior activity.

## Establish the target and existing state

1. Resolve the employer, exact role/requisition, live application URL, active campaign, packet ID, and tracking row. Open the live employer form; do not infer its identity from a tab group or previous file picker.
2. Check the ledger and existing receipts before any submission action. A missing recording does not mean an application was never submitted. If evidence conflicts, inspect the receipt or authenticated application status before retrying.
   For scheduled or multi-operator batches, first read [campaign coordination](../campaign/references/job-search-execution.md#coordinate-and-reconcile): claim the employer/requisition and shared capacity before action, respect the single browser owner, and count uncertain attempts against the shared cap. Reuse the [shared answer contract](../campaign/references/campaign-records.md#shared-answers-and-reviewed-templates) when completing fields.
3. Read the matching packet brief, application-fields file and tailored answers when present. Resolve absolute paths for the intended resume, cover letter, and portfolio link. Use current reviewed candidate facts; older resumes and recorded answers are evidence candidates, not automatic defaults.
4. Determine the requested endpoint. “Prepare/fill for review” stops before submission. Explicit permission to submit a named application or defined campaign carries forward; do not ask again solely because Submit is next. Use this plugin's `application-statements` guidance for a substantive answer that still needs drafting. This skill grants no permission to submit, send email, publish, or expand the campaign. If authorization is missing, finish reversible preparation and present the exact target, attachments, and answers for final approval.

## Complete and verify the form

- Use available browser/app tools and their documented upload mechanism. Prefer direct file-input upload when supported. With a native macOS picker, use Go to Folder and the exact absolute file path.
- Before accepting **each** file selection, compare live employer/role, packet ID, filename, and attachment field. If they disagree, cancel the picker and navigate to the right packet. Never trust the last-used directory.
- After upload, wait for completion and read the filename under the live attachment control. A selected file, Open click, or 100% progress indicator alone does not prove the correct attachment persisted. Remove any wrong attachment and verify its replacement.
- Adapt to the form: some accept cover-letter PDFs, others provide Additional Information. Use the matching tailored text and record its actual delivery method. Do not upload a deck into a resume field or attach every packet artifact merely because it exists.
- Fill required fields from reviewed evidence and the user's confirmed answers. Check autofill, dropdowns, character limits, required consents, and truncated text. Do not invent qualifications, salary expectations, work authorization, business-license status, demographic answers, or availability. Do not silently convert an hourly preference into an approved annual salary answer.
- For missing facts, record `[MISSING INFO: ...]` locally and ask one focused question; never submit that placeholder. Continue independent fields while waiting. Optional sensitive disclosures remain the user's choice.
- Handle email verification through the authorized account/tool or user input. Do not retain one-time codes in logs. Hand CAPTCHA or user-only verification to the user; do not bypass it. A disabled Submit button means a gate remains unresolved.
- Before submission, inspect the live employer/role, attachment names, contact fields, portfolio URL, screening answers, and remaining errors. Visually inspect changed documents before handing them off.

For screenshot-based review, keep 3–8 compact anchors: ID, source/viewport, approximate region, selector or AX hint if available, observed fact, intended action. Useful anchors are A1 employer heading, A2 resume control, A3 cover-letter control, A4 verification/Submit, and A5 confirmation. Refresh observations after navigation; coordinates are never reusable across employers.

## Submit once, then establish evidence

When authorized and ready, submit once and wait for a definitive response. Inspect validation failures and correct them. If a timeout, crash, or ambiguous response follows a submit click, check the current page, account status, and relevant receipt inbox before retrying. If acceptance remains unknown, preserve `submission uncertain` and the exact next check; do not repeatedly click Submit.

For employer-designated email applications, explicit send authorization is required. Verify recipient against the employer source, subject, body, and exact attachments before sending. Then inspect the sent message and attachment metadata. Do not turn an application into unrequested recruiter outreach.

Track evidence at its actual level:

| State | Required evidence | Limit |
|---|---|---|
| Prepared | Matching packet and form answers ready | Nothing transmitted |
| Attached / form ready | Expected filenames persisted in live form; required fields reviewed | No submission proof |
| Blocked / uncertain | Specific gate or ambiguous submit result recorded | Do not count as confirmed |
| Email sent | Sent-message evidence with correct recipient and attachments | Delivery, reading, and employer receipt remain unknown |
| Submission confirmed | Employer confirmation page, authenticated submitted status, or matching acknowledgment email | Does not imply interview or acceptance |
| Logged | Saved evidence and ledger agree; any existing generated tracker/dashboard is refreshed and verified | Logging is separate from submission |

Capture employer, role/job ID, channel, listing URL, exact attachment filenames, confirmation text, observation time with timezone, and evidence path or receipt reference. Distinguish observation time from exact submit time when the latter is unknown. A visible Submit button, packet publication receipt, or assistant status message is not an employer receipt.

Save minimal evidence in the existing private campaign location. Keep captures narrowly scoped; exclude security codes, authentication URLs/tokens, and unrelated inbox contents. Never place raw receipts or private tracking files in a public portfolio tree.

## Log, reconcile, and hand back

1. Update the existing record using job ID plus requisition/application URL to prevent duplicates. Preserve prior attempts, stronger evidence, and unrelated rows. Use the project's current schema; keep email-sent and employer-received distinctions in its fields or explicit evidence notes.
2. Save the receipt, then update the existing private source ledger and blocker/next-action record. Use `record_job_hunt_update` only when an installed runtime actually exposes it, and honor its confirmation contract. If unavailable, update the existing ledger directly under its own project instructions; for a new user without one, create the small private ledger described in [private workspace](../../references/private-workspace.md). Preserve prior rows and stronger evidence.
3. If a tracker/dashboard and its owning builder exist, regenerate the view from the source ledger using that builder. Do not patch generated counts or labels as a substitute for saving source data. If generation fails after submission, retain the receipt and report “submitted; dashboard update pending.” Do not resubmit. A new dashboard is not required for a single application or a ledger-only workspace.
4. Reopen saved evidence and the matching ledger record. Verify status and receipt/material links, plus the generated dashboard row and counts when a dashboard exists. Visually check changed anchors; use `ux-design-toolkit:design-studio` for design review only if its installed skill is actually discovered. Otherwise review 3–8 observed visual anchors against the task and recheck changed ones, without claiming a provider review. Count unique evidenced applications, identifying email-sent outcomes separately where the tracker combines them.
5. Close any automation-owned Chrome session and parent helper when necessary, preserving normal user tabs/processes. Verify no automation Chrome remains, or normal Chrome has a visible window without automation-only profile arguments. Only close processes whose ownership is established.
6. Report employer/role, exact submission state, receipt and tracking locations, and any remaining user action. Stop at the authorized endpoint; no new sourcing, portfolio redesign, publishing, or tooling lane is implied.

Completion means the authorized endpoint is evidenced and its tracking is saved. A blocked outcome is a documented handoff, not a completed submission.

For document, PDF, slide, website, visual, and publishing work, use the current [provider boundary](../../references/providers.md) only when that output is requested.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Career Strategist, Job Search Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
