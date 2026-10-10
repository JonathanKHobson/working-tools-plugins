# Native Gmail scheduling and batch verification

Use for requested scheduled mail or a personalized batch. Reuse the already completed voice/editorial review for unchanged shared copy. Review each actual recipient, greeting, changed passage, subject, sender and private link before scheduling. Multiple people may intentionally share one address; reconcile intended messages, not merely address counts.

## Resolve the execution surface

Confirm the account in the actual composer. The connected Gmail API and visible browser can be signed into different accounts; an account index such as `/u/1` is not an identity. Prefer the actual provider capability when it supports the requested action; use native Gmail UI when scheduling is not exposed. Do not replace scheduling with immediate sending or an agent automation.

Use an absolute date, local time and named user time zone. Confirm the scheduler's displayed date and zone, especially near midnight or daylight-saving boundaries. A preset such as “Tomorrow morning” is acceptable only when its displayed date/time matches the requested result.

## Commit one message at a time

1. Reuse a saved draft if one exists; identify it by recipient and subject. Before filling, confirm which composer is active. Scope locators to that specific composer, and ensure pasted HTML is rendered content rather than literal source text.
2. Check the actual draft's sender, To/Cc/Bcc, subject, body, attachments and links. Do not rely on a source HTML file or an in-memory recipient counter. Sample visual rendering of the shared template and check materially different variants.
3. Choose native Schedule send and the verified date/time. Wait for the composer to close, then read the result. **Composer disappearance, an optimistic toast and an incremented Scheduled count can be rolled back after a delayed network failure.** Confirm the message persists in Scheduled with the correct recipient, subject and date/time before progressing to the next draft. Refresh/revisit if the result is ambiguous.
4. If Gmail restores a composer with a failure alert, stop entering the next person's fields. Preserve drafts with Save & close when necessary, inspect Scheduled for the affected message, and reopen the matching draft only if it is absent. Re-read its contents: a late-restored composer can steal focus, leaving the next recipient's address in the previous body. Repair that contamination before retrying. Never blindly resend or create a second copy.
5. After a batch, reconcile the full intended message ledger against persisted scheduled rows or message details. Capture recipient, subject, absolute time/zone and available provider identifier/link. Counts are a cross-check, not proof of the recipient set. Preserve pre-existing unrelated scheduled messages. Check changed/failed variants explicitly.

Stop and preserve recoverable drafts if provider state remains ambiguous or repeated failures prevent reliable verification. Report exactly what is verified scheduled and what remains drafted; do not continue uncontrolled retries.

## Review and evidence boundary

The local `gate.py` covers registered connector send actions, not browser clicks. Never manufacture a tool name or fingerprint to claim a UI scheduling gate ran. Record the manual final review and actual Scheduled readback in the owning project's existing delivery record; private capability links need not be copied into that record. A draft-only or approval hold stays in place.

Keep archived EML, source HTML and screenshots labeled as preparation evidence. A later copy/link edit invalidates the relevant previous visual check. `SENT` or a sent-message readback proves the provider's sent state; it does not prove recipient inbox arrival or reading. Scheduled messages are not yet sent. State remaining delivery dependencies plainly.
