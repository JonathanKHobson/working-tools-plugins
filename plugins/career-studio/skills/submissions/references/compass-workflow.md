# Private campaign execution

Resolve the existing workspace through [private workspace](../../../references/private-workspace.md). Locate its active campaign, source ledger, packet directory, question/answer records and receipt store where present. Locate a dashboard builder only if that workspace uses one. Paths and field names are project contracts, not fixed plugin defaults.

When a builder exists, inspect its current arguments and dependencies before running it. Update the source record first, then regenerate the existing web dashboard when needed. If there is no builder, save and reopen the existing private ledger, or the small private ledger for a new user, with the receipt reference and state; do not imply a generated dashboard was validated. A workbook may be an optional export; it must not silently replace the user's primary dashboard. If generation fails after a confirmed submission, retain the receipt and repair the view without resubmitting.

Minimal receipt fields are employer, exact role/requisition, application URL, channel, attachment identities, confirmation observation, timestamp with basis, and evidence reference. Store only what is needed; omit verification codes, auth URLs and unrelated inbox contents. Preserve the distinction between email Sent evidence and employer acknowledgment even if the existing ledger uses one broad submitted label.

Check these failure cases: wrong employer in the file picker; matching attachments with unresolved verification; an old receipt plus a reopened form; timeout after a submit click; uncertain employer acknowledgment; valid receipt with a failed dashboard refresh; and a user request to fill for review. Each calls for a different state or next action. None justifies blind resubmission.
