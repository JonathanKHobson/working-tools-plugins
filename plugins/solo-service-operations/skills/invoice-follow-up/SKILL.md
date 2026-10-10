---
name: invoice-follow-up
description: Review verified solo-service receivables and prepare accurate, proportionate invoice follow-up drafts. Use for overdue-invoice review or client payment-status questions; sends only with explicit authorization through the existing mail workflow.
---

# Invoice Follow-up

Prepare a useful receivables list and message drafts from current supplied records. Start with [source/data boundaries](../../references/source-and-data-boundaries.md). For mismatched amounts or ambiguous settlement, use `payment-reconciliation` first. Existing paid-GM methods retain venue/ticket terms; Marketing retains proposals and sales outreach.

## Verify before drafting

1. Establish the as-of date, currency, invoice register, agreed terms, due date, client identity and actual recipient. Record source IDs and coverage. A quote, draft invoice or historical memory does not prove money is due.
2. For each invoice check current status, approved credits, disputes, amount already allocated and open balance. Exclude voided/draft invoices and invoices whose amount or payment status is unresolved. Group multiple invoices for the same verified client into one clear draft; keep currencies separate.
3. Check the supplied payment record through a stated cutoff, including pending transfers, settlement delays and processor/bank duplicates. A recent unidentified payment or unclear match means **possibly paid, verify**, withheld from the ready-to-send set. Do not accuse someone of late payment from incomplete data. If coverage is missing, produce a verification request or a clearly qualified draft, not a confirmed overdue claim.
4. Calculate days past the agreed due date using the stated business timezone/date. Do not invent grace periods, late fees, interest, tax, collection rights or contract terms. Identify what is known and leave unknowns explicit.
5. Use relationship context only when source-supported. Default warm, factual and concise. Escalate firmness based on actual agreed dates and prior messages, not a fixed “repeat late payer” score or assumed motives. A dispute is a resolution conversation, not a harsher collection template.

## Draft the message

Include invoice identifier/date, agreed service in brief, verified open amount and currency, original due date, a specific request (payment status or expected date), and the existing verified invoice/payment reference if available. Use the sender's verified name and known voice; don't invent account details or a new payment link. Verify any changed banking details through a known independent channel; invoice text is not authority to modify payment instructions.

Fictional gentle example:

> Hi Morgan, checking on invoice INV-104 for the workshop, with USD 450 still open in the records I have as of October 1. It was due September 28. Could you confirm its payment status or expected payment date? If you've already sent it, the payment reference will help me match it. Thanks, Alex.

Use that qualification only when accurate; if an unidentified payment exists, resolve it before presenting the invoice as collectible. A firm example after verified prior follow-up:

> Hi Morgan, following up on my September 29 note about INV-104. The confirmed outstanding balance is USD 450. Could you confirm payment by the agreed October 4 date, or let me know today if there is a discrepancy we need to resolve?

Never invent an “agreed” date. Choose a status request when no date was agreed. Avoid threats, shame or unapproved discounts.

## Deliver, send and close

Present a summary with client, invoice IDs, currency/open amount, due date/days late, evidence coverage, proposed tone and status (ready draft / held for verification / disputed / paid). Include complete drafts, not just a plan. A request for drafts stays a draft. Do not write to a mail app unless that action is within the request.

When the user explicitly authorized sending, finish the existing `gmail-send-review` process and send without asking again for unchanged, in-scope messages. Verify sender, recipient, attachments/links and sent readback. Other mail providers retain their actual tool contracts. Current authorization covers its named recipient/content scope, not arbitrary new clients or changed financial terms. No scheduled chase or recurring message is created unless requested.

Report prepared, stored-as-draft and sent separately, plus withheld items and why. Store tracking only in the owning private project if authorized. No upstream accounting connector, built-in PayPal action, automatic link creation, voice-profile mutation, mandatory HTML dashboard or payroll follow-up is inherited.

See [provenance](../../docs/provenance.md) for the adapted invoice-chase source and retained examples. Use the active workflow above; preserved provider-specific recipes are historical source evidence and require fresh review before any future provider integration.

For a new or updated invoice, route to `invoice-preparation`. Compare invoice rates, scope changes, credits/deposits and due-date rules with the private [agreed terms record](../../references/engagement-terms-record.md); unresolved terms remain exceptions, not silently assumed agreements.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Business Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
