---
name: invoice-preparation
description: Prepare or update evidence-backed solo-service invoices, using agreed terms, active-human-work evidence and a supplied document template. Use for compiling billable work or creating invoice review copies; keeps estimates, approval, sending and payment distinct. Also use for a concise “what can this plugin do/how do I get started?” answer; route specific tasks to the matching specialist.
---

# Invoice Preparation

If asked what Solo Service Operations Studio can do or how to start, use the [human guide](../../README.md) to distinguish invoice preparation, follow-up, payment matching, and cash timing. Offer a first task with the specific private records needed and a reviewable result. If a task is already specified, route directly; do not imply connected accounting access or remembered client data.

Turn agreed work and dated evidence into a correct, reviewable invoice. Existing client workflows remain authoritative for their document layout and calculation method. Start with [existing client workflow routing](../../references/client-workflows.md) and the selected private project. Client evidence, terms and current invoice state belong in that project, not this plugin.

1. Establish client, invoice number, service period, timezone, evidence cutoff, currency and requested deliverable. Distinguish new invoice, incremental work update and formatting-only edit. Preserve approved invoices and user edits; snapshot before replacing a current draft. Never reconstruct hours during a formatting-only request.
2. Read or create the smallest [agreed terms record](../../references/engagement-terms-record.md) from actual agreement evidence. Compare rate, billing basis, scope, approved changes, deposits/credits and due-date rule. Unknown or conflicting terms remain unresolved; an old invoice is a useful precedent, not proof of current agreement. Do not invent tax, late fees, acceptance or payment instructions.
3. Collect a bounded [work-evidence ledger](../../references/work-evidence.md). Prefer confirmed time; reconstruct only with explicit internal basis and uncertainty. Combine Figma, client messages, meetings, project conversations and file evidence by work package. Activities and outputs are not interchangeable: active exploration, review and unfinished iterations can be valid work. An assignment, open window or completed AI response alone does not prove the user spent that time.
4. Compare with the last final/sent invoice and any current draft. Check period boundaries and stable item IDs, previously billed work and deposits; never double bill the same package or add Computer History intervals on top of its estimated hours. Keep anticipated work separate internally and include it only when authorized. No arbitrary target from past monthly totals.
5. Build one structured source of truth containing item ID/code, service description, source IDs, completion status, hours/basis, rate and amount, plus invoice metadata. Preserve quarter-hours exactly. Calculate money with Decimal and make the rounding rule explicit. Flat-fee services retain their agreed basis rather than fabricated hours. Leave missing facts visible in a review copy.
6. Use the existing client builder and retained template when present. For requested documents, use a separately available document builder and the client's supplied or authorized template. Read its retained reference; replace all historical invoice data. The template supplies design, never current billing facts. See the existing client route before choosing its script input.
7. Independently reconcile every line, summary, exhibit, credits and payable with source data. Recheck hours, rate and due date against terms. Render every page, inspect identity, metadata, summary, exhibit headings/tables, full descriptions and footers. Do not shrink away content to imitate the old page count. Return the requested file with total/delta, evidence coverage, calculation/render verification and material unresolved items.

Use Writing Quality Studio's communication owner for client prose; preserve technical/product terms and factual detail. Drafting an invoice does not authorize Gmail writes or sending. If sending is explicitly requested, complete `gmail-send-review` and verify the sent message and attachment. Historical scheduling or approval is not a new send instruction. Invoice approval is not payment. Without complete payment coverage, label payment status **unknown / not verified**, never unpaid or overdue merely because no receipt was supplied; route actual settlement to `payment-reconciliation`, verified overdue administration to `invoice-follow-up`, and timing projections to `cash-flow-planning`.

## Completion example

Fictional: a user-confirmed 2-hour design package includes a reviewed 45-minute Figma interval plus messages and a Loom review about that same work. Billable basis remains 2 hours, not 2.75. A separate 30-minute confirmed client meeting can be another line if within scope and not already included. Show the link and uncertainty internally; use concise service descriptions in the invoice.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Business Operations Specialist, Business Advisor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
