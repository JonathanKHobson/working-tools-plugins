# Event email operations

Use when an authorized event follow-up spans calendar guests, attendance, registration sources, a contact database or opt-out handling. Writing Quality owns copy; the actual mail provider owns scheduling and delivery. Do not introduce a new CRM, queue or mailing service if the existing system can complete the task.

## Reconcile the audience once

Build one project-owned ledger from the named event's live sources. Preserve source and eligibility evidence, verified names and exclusions. Do not import unrelated prior-event recipients merely because their addresses occur in a previous email. Preserve distinctions among invited, registered, attended and explicitly subscribed. Importing a contact does not establish newsletter consent.

Normalize whitespace and compare addresses case-insensitively while preserving their supplied spelling. Do not silently repair typos, strip plus tags or infer that two different addresses are the same person. Deduplicate overlapping records for the same intended person/message. A shared household address can legitimately receive separate personalized messages for two people when the user requested that; reconcile message keys as well as unique addresses. Group aliases and an individual forwarding request are separate audiences. Keep recipients private through individual messages or an authorized BCC group.

Resolve relative send dates against the user's time zone and event context. If the user delegates an ambiguous choice, state the chosen absolute date and continue; do not reopen the same question. Recheck the provider's displayed zone and date at scheduling time. Do not substitute an agent reminder for native provider scheduling when native scheduling was requested.

## Opt-out means a verified change

Define which list or membership the opt-out controls. Removing a contact, blocking future promotional email, revoking course access, deleting registration history and leaving an external community are different actions. A minimal suppression record is usually needed to prevent a later import from re-adding an opted-out address; keep only the data required for that purpose under the applicable retention policy.

Use the existing preferences mechanism where possible. Personal links must not expose another recipient's token. A shared/forwarded email needs a general preferences form with identity verification rather than a one-click link that removes the original recipient. Do not perform opt-out as a side effect of a GET request that a link scanner can follow. For a newly built flow, test with an organizer-owned alias: confirmed action, mailing-list removal, durable suppression, blocked re-import/queued mail where supported, and requested organizer notification. Queue creation or provider acceptance is not an inbox receipt.

Inventory already scheduled messages as well as future database sends. A website suppression record does not automatically cancel native Gmail schedules. When the user has authorized an opt-out, cancel matching pending schedules through the provider and verify their removal; preserve messages outside that opt-out's person/address/list scope, including a different household participant where applicable. Do not claim a universal opt-out integration if only one system was tested.

For compliance questions, verify current requirements for the actual message, jurisdiction and provider using authoritative sources. Free admission alone does not settle whether a message is commercial. A city or email address is not a substitute when a postal address is required. Do not publish a private home address without clear direction. Avoid blanket claims of compliance or spam-filter immunity from copy/layout alone; body unsubscribe links and provider-level List-Unsubscribe headers are different capabilities.

## Close with evidence

Reconcile intended messages against the provider's persisted recipient, subject and scheduled date/time or sent-message records. Preserve unrelated scheduled mail. Record exclusions and any unverifiable recipient names without exposing the entire list in a public summary. Report prepared, scheduled, sent, provider-accepted and inbox-received states separately. Keep contact data, private links and current campaign receipts in the project, not in plugin examples.
