# Campaign records and evidence contract

Read when starting/resuming or reconciling status. Map these logical fields onto existing storage; this is not a mandatory schema migration.

## Observed layout

These paths are relative to `applications/<active-campaign>/`. Inspect current files before reusing conventions elsewhere.

| Path | Responsibility |
| --- | --- |
| `research/*-jobs.json` | Role identity, listing sources, fit and priority inputs |
| `private/packets.json` | Job ID, packet directory, materials, portfolio/publication state |
| `private/submissions.json` | Submission channel, dates, attachments, confirmation/evidence |
| `private/blockers.json` | Open/resolved issues, required action, independent work |
| `private/outreach.json` | Separate outreach records; not application receipts |
| `private/questions-and-handoff.md` | Unresolved facts, scoped approvals, recovery context |
| `packets/<job-id>/` | Employer-specific working/final materials and form responses |
| `qa/*-submission-receipt.json` | Private observations and supporting evidence pointers |
| `qa/*-publication-receipt.json` | Portfolio publication evidence, never application evidence |
| `scripts/build_tracker.mjs` | Existing generator reading source records into derived views |
| `dashboard/`, `outputs/` | Derived dashboard, tracker and analysis exports |

Resolve the current preference source from project files rather than inferring preferences from old applications. Do not patch only generated dashboard values. Inspect generator arguments, output paths and dependencies before running it. Keep mutable source state separate from dated snapshots. Reread before writing and preserve concurrent changes.

## Minimum information per role

| Group | Capture |
| --- | --- |
| Identity | Job ID, employer, exact title, requisition/listing URL, application URL, track |
| Decision | Listing status/check time, fit rationale, location/work mode, pay source and units |
| Materials | Packet directory; exact resume/letter/response paths; required/optional list; version or modified time; review state; portfolio URL/visibility |
| Answers | Question text or field ID, answer, evidence/user confirmation, unresolved gaps |
| Coordination | Owner/scheduled run ID; employer/requisition claim; browser owner; reserved slot; attempt state/time; release or handoff evidence; canonical writer and worker delta provenance |
| Authorization | Scope already granted and source reference; new decisions required |
| Attachments | Intended and displayed filenames, processing/result, observation time/evidence |
| Blocker | ID, job or campaign scope, issue, owner, action needed, status, observation time, independent work, resolution evidence |
| Submission | Channel, status, attempt time, supported submitted/sent time, actor if known, attached versus linked materials |
| Receipt | Kind, source path/message ID or safe URL, employer/requisition match, short acknowledgment, observed time and timestamp basis |
| Continuation | One next action, owner, updated time; follow-up date only when chosen/requested |

Store only necessary private application data. Exclude passwords, codes, tokens, OAuth callback parameters, unrelated contacts and raw history. Sanitize receipt URLs. Use evidence references rather than copying full mailboxes/event streams.

## Shared answers and reviewed templates

Keep one shared answer source for all authorized operators in the private campaign's existing records. For each reusable answer, retain the exact question or field meaning, answer, supporting source ID/path or explicit user confirmation, confirmed/reviewed date, applicability scope (employer, role, jurisdiction, pay unit or time period as relevant), and unresolved gaps. Store question-dependent answers by meaning, not a bare yes/no. A source candidate or old portal entry is not automatically a reviewed current fact.

Reuse an answer only when the new question and its scope match and the fact is still current. Reconfirm when wording changes its meaning, an employer/jurisdiction changes eligibility, pay unit or compensation range changes, availability/relocation/travel creates a new commitment, evidence conflicts or is stale, or consent/sensitive disclosure is being requested. Ask only for the affected missing fact; preserve unchanged reviewed answers. Do not infer unknown answers from prior applications or nearby evidence. Keep `[MISSING INFO: ...]` private and block the affected submission until resolved.

Reviewed reusable material records should point to source evidence, version/review date and allowed scope. Role-specific packets must identify which reviewed sections/templates they used and their final employer/requisition. Do not overwrite finished packets with generator scaffolds. Store experiment hypothesis, variant IDs and observed outcomes beside existing campaign/run records only when a comparison is requested; the source skill holds the method, not personal variants or results.

## Separate state dimensions

| Dimension | Useful states | Evidence threshold |
| --- | --- | --- |
| Listing | unknown, verified-open, closed | Current official listing; historical listing is dated evidence |
| Materials | missing, draft, ready | Required final files exist and content/visual checks passed |
| Upload | not-started, selected, attached-verified, failed | Matching displayed filenames and successful processing for attached-verified |
| Submission | not-started, attempted-unconfirmed, sent-verified, submitted-confirmed | Actual Sent evidence for sent; employer/ATS acknowledgment tied to application for confirmed |
| Receipt | none, reported-only, employer-confirmed | Reports remain reported until source verification |
| Blocker | open, resolved | Successful affected step or direct resolution evidence |

A role can have ready materials, verified attachments, an attempted-unconfirmed submission, and an open verification blocker simultaneously. Do not collapse these into “done.” Where a schema uses `submitted`, preserve it but require confirmation evidence for that interpretation; use supported evidence/notes fields for detail.

Use observation time for when evidence was seen. Give submission timestamps a basis; when exact submit time is unavailable, label confirmation observation time. Retain conflicting records with provenance until resolved. Historical evidence verifies a historical state, not current listing availability.

## Fallback without an existing tracker

Create one private Markdown ledger rather than a tracking application. One row per role: ID; employer/role/link; material paths/readiness; upload state; submission/channel; receipt source; blocker/owner; next action; updated time. Put detailed questions, authorization and observations beneath each ID. Split a receipt into a file only when evidence needs it.

## Reconciliation examples

- Correct PDF selected in picker: selected; submission not-started unless another source shows an attempt.
- Matching PDFs visible but verification unresolved: attached-verified and open blocker; submission not-started or attempted-unconfirmed according to the observed action.
- Employer acknowledgment at the matching requisition URL: submitted-confirmed and employer-confirmed receipt; retain source/time.
- Email in Sent with correct recipient/files: sent-verified; receipt none until employer acknowledgment.
- Chat says nine completed but evidence covers one: retain reported total as historical context; verify role-level records before claiming nine confirmed.
- Existing receipt plus a reopened form: reconcile first; opening the form neither erases the receipt nor authorizes duplicate submission.
