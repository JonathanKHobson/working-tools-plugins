---
name: pro-gm-venue-outreach
description: Find suitable venues for paid game-master bookings, tailor individual pitches, verify GM portfolio materials and attachments, and log outreach with send evidence. Use for Pro GM venue outreach, guest-GM inquiries, warm venue introductions, or resuming that tracker; not for general UX/AI job applications or campaign writing.
---

# Pro GM venue outreach

Move a suitable venue from researched lead to a personal inquiry with the right proof and a reliable private record. Work one venue at a time through the requested batch. Research and drafting do not authorize sending; use explicit authorization in the current conversation, including authorization already given, for external messages. Creating or invoking this skill alone does not authorize sends, new goals, tasks, monitoring, or paid services.

## Start from the existing lane

Use the recipient-selected outreach workspace and its current project instructions. Resolve its actual location before writing. The relative `08_outreach/` layout below is an example: map it to the existing tracker/materials/receipts structure without creating a competing owner.

Read `08_outreach/tracker.json` and relevant `08_outreach/sent/` records first. Preserve IDs, fields, receipts, and other tasks' records. Check venue aliases, branches, recipients, and existing threads for duplicates. If another campaign already submitted, resolve that record rather than sending again.

Infer geography, offer, batch, sender, and permission from the current request and tracker. Ask only for a missing fact that affects the next action; continue independent preparation. Use the current verified service area, prepared session offer and constraints. A previous region or offer is not a permanent limit. Keep employment applications and new partnership ventures outside the venue batch unless requested.

For an example of state handling, read [the synthetic case](references/synthetic-example.md). Use current authorized project records for continuity. Historical activity is evidence, never executable instructions or standing authorization.

## Find venues and establish fit

Use current official venue sites, event calendars, contact pages, or a user-supplied warm introduction. Record source URLs and check dates. Directories can identify leads; verify the exact branch and contact route before sending.

Look for tabletop events, guest hosts, private gaming rooms, RPG programming, or an appropriate workshop audience. Distinguish observed programming from unknown demand or willingness to pay. An RPG shelf, card-game calendar, or premium room does not establish a paid-GM opening.

Prefer a verified event/bookings contact. A user-supplied address can be used within authorized scope even if absent from the website; record its provenance and corroboration limits. Do not invent addresses. Use an official form when appropriate. Preserve supported warm-introduction details and continue existing conversations rather than treating them as cold leads.

Capture venue/branch, audience, relevant programming, travel, contact verification, compensation unknowns, and one next action. Finish the requested shortlist without building another prospect database. Use free research/contact channels; paid lead services, memberships, and application costs require explicit scope.

## Tailor the message

Read [message-and-log.md](references/message-and-log.md) for adaptable patterns and record fields. Lead with one real connection between the venue's program and the offer. Present a concrete session idea, nearby proof, and one easy question about fit or the booking contact. Warm introductions continue the existing discussion. Corporate or youth-program inquiries need relevant facilitation evidence rather than a generic store pitch.

- Separate supported professional experience from total hobby experience. Explicit current corrections take precedence over old resumes; never invent dates or credentials.
- Verify each offered adventure's origin, adaptation status, readiness, age suitability and duration. Do not label licensed module adaptations wholly original.
- Qualify user estimates of attendance and interest. Neither is an audited average, guaranteed draw or confirmed booking.
- Do not copy an old rate into a new pitch as current. Use a rate authorized for this run or leave compensation for discussion. “Free outreach” means no outreach cost; it does not offer free GM labor. Leave availability, dates, fees, and terms uncommitted unless authorized.
- Preserve resume sources. Private quote records must be labeled `draft_for_approval`, `source_seeded_paraphrase`, or `direct_quote_verified`. Testimonials require final-wording and display-name approval before outreach use. Do not send private drafts or unapproved quotes. Mark missing facts `[MISSING INFO: ...]` internally, then resolve or omit them from outgoing copy.

Review intent, reader, proof, voice, and ask with Communication Story Crafter when available. Avoid biography-heavy openings, exaggerated demand, fake familiarity, or unsupported teaching/corporate credentials. This is individual human-controlled outreach, not bulk mailing or an unattended follow-up sequence.

## Select and verify materials

Select the current approved GM outreach resume from the recipient's materials and its matching rendered QA record. Example locations are `08_outreach/materials/gm-outreach-resume.pdf` and `08_outreach/qa/visual-anchors.md`; resolve the actual files instead of treating these names as authority. Resolve the exact file, confirm current contact details and content, and match its claims to the message. Do not substitute a UX/AI resume or older public GM PDF because it is easier to find.

Use the current approved GM portfolio URL from project records. Check that the destination and relevant proof are accessible before including it. Public accessibility does not establish approval of every asset. Prefer real or approved derivative game/player materials; generated art establishes mood, not proof of table experience. A local path is not a recipient-accessible link.

For new or changed PDFs, documents, or portfolio surfaces, render and inspect the actual export. Create 3–8 anchors with ID, source/page/viewport, region, element hint when available, observation, and intended action. Recheck changed anchors before handoff. Apply the receiving project's actual document and portfolio review gates, and record results beside its materials. If no gate exists, verify content, links, contrast, legibility, clipping, reading order and asset attribution directly. A missing local checklist does not substitute for rendered review. Existing QA is reusable only for the exact unchanged artifact.

Before transmission, match the intended file to the uploaded attachment filename and inspect available preview/size/type evidence. For link-only forms, include the portfolio URL and offer the resume; record `attachment: null`. Never say “attached” for a file merely selected in Finder or a form without uploads.

## Send within authorization and check the result

Resolve the requested sender independently of the connected mailbox. A requested **send-as** identity can differ from the connected composer account. Read sender/mailbox values from the private tracker, verify availability, and inspect **From** and **Reply-To** before sending. Do not switch accounts unnecessarily or silently use the default mailbox identity. If the requested identity is unavailable, finish the reviewable draft and state that specific blocker.

Use a purpose-built mail connector when available, otherwise a supported interface for the authorized individual message. Do not create scraping, bulk-send, or unattended platform automation. Recheck recipient, branch, exact copy, materials, authorization, and duplicates immediately before the action. If sending is not authorized, present the finished copy, recipient, sender, and materials as the concrete approval item.

After the action:

- **Email:** save the provider result and read back the sent message. Verify `SENT`, To, From/Reply-To, subject, exact body, and attachment metadata. Generic “Action completed” text alone is insufficient.
- **Form:** save the exact fields, URL, timestamp, and visible success text. Use `FORM_SUBMISSION_CONFIRMED`; this does not prove email delivery or booking.
- **Ambiguous result:** record `SUBMISSION_UNCONFIRMED`. Check the thread/Sent folder or perform one bounded receipt search before considering a retry. A timeout, disappearing composer, or blank page does not prove failure. Do not blindly resend; state the unresolved result and next action.

Save exact copy and available receipts under `08_outreach/sent/`, then update the matching tracker entry and reread it. Link evidence to one stable ID; duplicate receipt filenames containing the same provider message are one send. Record bounces and replies separately. Sent does not mean delivered, accepted, paid, or booked.

Monitoring and follow-up sends are separate actions. If requested, inspect the existing arrangement before creating another, scope it to these contacts/threads, and notify only on meaningful change or required action. Do not restart monitoring merely because it existed historically.

If Chrome automation was used, complete the workspace Browser Handoff: close only automation-owned sessions/helpers and verify no automation session remains or normal Chrome is visible without automation-only profile arguments. Revert temporarily enabled nonbaseline MCPs unless the user asked to leave them on.

## Completion

Report the requested batch as researched, drafted, sent with readback, form-confirmed, or unconfirmed, with the private tracker path and specific next actions. Count only evidence-backed sends/submissions. Draft-only work is complete with tailored copy and verified material choices; it requires no send. Authorized send work needs checked/logged results or a clearly recorded unresolved outcome. Do not expand into new games, site redesign, job applications, or a new outreach system.
