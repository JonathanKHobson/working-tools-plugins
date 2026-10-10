---
title: Venue message patterns and private records
type: skill-reference
status: active
tags: [pro-gm, outreach, private, communication]
---

# Message patterns and private records

These are drafting aids, not approved messages. Replace bracketed fields with verified facts and omit unsupported optional claims.

## Venue inquiry

Subject: Paid [system] one-shot at [venue/branch]

Hi [events team or verified name],

[One specific, current fact about their program] made me think a [specific prepared session] could fit your audience. I'm [your name], [brief supported GM context].

I can bring [verified game/materials offer]. [Optional concise proof or authorized compensation framing.] Would a paid guest-GM session fit your programming, and are you the right person to discuss it with?

[My GM resume is attached , only after attachment verification.] The portfolio includes [relevant actual materials]: [verified portfolio URL].

Thanks,
[Your name]

## Warm introduction

Subject: [Verified introducer]'s introduction , [shared topic]

Hi [name],

[Verified introducer] suggested I contact you after [actual conversation/context]. I'm interested in [the opportunity actually discussed].

[One or two supported capabilities and their connection to the recipient's program.] Would you be open to a short conversation about [one concrete decision]?

[Appropriate resume attachment statement or offer.] [Portfolio link.]

Thanks,
[Your name]

For forms with no upload, use “I can also send my GM resume.” Keep workshop/chapter discussions exploratory; an introduction is not a partnership agreement or authorization to form an organization.

## Tracker compatibility

Reuse `08_outreach/tracker.json`; do not replace its schema or reinitialize it. A compatible example top-level structure is `owner_thread_id`, `sender`, `mailbox`, `created_at`, `entries`, and `leads`. Preserve fields you do not own and reread before saving if another task may be active. Add only useful missing fields to the affected record.

| Record group | Fields or evidence |
| --- | --- |
| Identity | Stable `id`, `key`, `venue` including branch, `kind` |
| Fit | `source`, optional `fit_source`, check date, `contact_verification`, `fit`, `travel`, `payment` with proposed/unagreed distinction |
| Message | `to` or form URL, `subject`, sender/Reply-To, `copy` path to exact text and receipt |
| Materials | Exact filename/path, optional hash, upload/readback metadata, portfolio URL; null attachment for link-only forms |
| Permission | Current user instruction authorizing the send; no inferred standing permission |
| Result | `status`, sent/submitted/attempt timestamp, `message_id`, `thread_id`, or exact form `confirmation` |
| Continuation | `reply`, `next_action`, `blockers`; monitor details only when actually configured |

Paths are relative to `08_outreach/`, e.g. `sent/gm-out-006-venue.json`. Choose the next unused ID after reading the ledger; do not blindly reuse an example number. Label drafts explicitly and keep them separate from exact sent copy. Retain originals when recording corrections or resends.

## Evidence states

| State | Sufficient evidence | Insufficient evidence |
| --- | --- | --- |
| `RESEARCHED` | Current branch/contact source and candid fit assessment | Search snippet treated as confirmed opportunity |
| `DRAFTED` | Recipient-specific copy and selected materials; no transmission claim | Template with unresolved outgoing placeholders |
| `SENT` | Provider sent record/readback with matching headers, copy, and intended attachment | Clicked Send, selected file, or generic success alone |
| `FORM_SUBMISSION_CONFIRMED` | Official success after submission; exact fields saved | Filled form, navigation away, predicted success URL |
| `SUBMISSION_UNCONFIRMED` | Attempt with no conclusive result after bounded check | Assumption of failure followed by automatic resend |

If transmission is known but attachment verification is incomplete, record that limitation; do not call the packet fully verified or automatically resend it. Delivery, replies, and booking agreements require separate evidence. Preserve existing application-specific states without enrolling employment applications into the venue workflow.

The exact-copy record should include body/fields, channel, source URL or recipient, chosen sender, materials, action time, provider IDs, and verification. Save only evidence needed for continuity, not raw inboxes, credentials, or unrelated personal conversations.
