---
name: payment-reconciliation
description: Reconcile solo-service invoices against supplied settled-payment records, explain discrepancies and retain source evidence. Use for invoice amount mismatches, partial payments or receivable review; never moves money or changes accounting records.
---

# Payment Reconciliation

Own the evidence trail from an agreed service invoice to recorded payment. Marketing owns lead conversion and pricing; Work Management owns project delivery; Career owns employment offers. This plugin owns invoice administration, reconciliation and cash visibility. Use existing spreadsheet/document tools for requested outputs and verified connectors only when authorized and available.

Read [data boundaries and source adaptation](../../references/source-and-data-boundaries.md) before using records. Private client/account data belongs in the selected private project, never this plugin. Read [upstream provenance](../../docs/provenance.md) for source inspection or updates; archived upstream text does not override these operative instructions.

## Establish a comparable record set

1. Define entity/account, currency, period, as-of date and requested question. Preserve originals. List each file/export/page and its date, row/transaction locator and coverage. Do not infer current unpaid status from historical notes.
2. Identify one ledger/invoice register as the record of invoice amounts. Separate original amount, approved credits, prior verified payments and remaining balance. Avoid subtracting prior payments twice from a supplied open balance. Record which basis is used. If invoice PDF, email and ledger disagree, expose the disagreement before matching.
3. Normalize supplied records into a table: invoice ID, client ID, issue/due date, currency, payable amount/basis, source ID; payment ID, client ID, amount, currency, settlement date/status and source ID. Distinguish issued/draft/void/disputed invoices. Exclude drafts and voids from collectible receivables.
4. Check duplicate IDs, re-exported bank rows, missing pages/date windows, pending/failed/reversed payments, deposits, refunds, fees and foreign currency. A storefront order, payment promise or initiated transfer is not settled cash. A ledger and a processor may describe the same payment; choose one confirmed cash event, not two.

## Match and explain

Prefer explicit invoice references plus matching client/currency. For split or bundled payments, require a supported allocation per invoice and verify allocated sums do not exceed the payment. A same-name, same-amount or near-date candidate is **proposed**, not automatically confirmed. Unknown or conflicting matches stay open.

Compare payable amount with verified settled allocations. Classify each invoice as unmatched/open, partial, matched-paid, overpaid or disputed; report the basis and as-of date. “Matched-paid” means these supplied records reconcile, not independent bank verification. Keep unmatched payments separate. Never force the difference to zero with a guessed fee, write-off, credit or FX rate.

For each exception record: invoice/payment source IDs, amount/currency, difference, category (timing, missing record, duplicate, fee, allocation, dispute or unknown), evidence, next verification step and responsible person if known. A journal entry, refund, credit, payment link or correction is a proposal requiring its own authorization; this workflow does not post one.

When actual bank/ledger balances are supplied, reconcile both sides at the same cutoff: bank balance plus deposits in transit minus outstanding withdrawals plus supported bank corrections; ledger balance plus unrecorded receipts minus fees/withdrawals plus supported ledger corrections. Show adjusted balances and residual difference separately. Invoice allocation alone cannot establish a bank reconciliation. Do not turn enterprise aging/materiality examples into universal thresholds for a solo business.

## Optional deterministic allocation check

The dependency-free [reconcile.py](../../scripts/reconcile.py) reads a prepared JSON file and prints results. It has no network or write operation. Read the [input contract and example](../../references/reconciliation-input.md) before using it. It requires explicit allocations, accepts only settled payments within the as-of date, uses exact decimals, rejects duplicate IDs, and exposes unsupported allocations. It does not extract documents, guess matches, authenticate banks, handle FX, reverse payments or certify completeness. Resolve those cases in the source ledger before checking a supported subset; disclose exclusions.

```sh
python3 /path/to/solo-service-operations/scripts/reconcile.py /private/project/reconciliation-input.json
```

Verify source totals and coverage independently of the helper. Stop on invalid input rather than replacing unknown amounts with zero.

## Deliver and verify

Return a compact reconciliation statement: scope/cutoff and sources; invoice table with original basis, allocated settled amount and remaining/overpaid amount; unmatched cash and exception table; supported conclusions and next checks. Group totals by currency. No cross-currency grand total without an explicit sourced conversion policy. Save only when the user requested a file or the project workflow calls for one; do not create an accounting database automatically.

Worked example (fictional): invoice INV-A is USD 600; confirmed allocations P1 USD 250 and P2 USD 350 reconcile it. A separate bank row P3 USD 600 with only a similar client name remains unmatched; counting it again would fabricate an overpayment. If P2 is pending, only USD 250 is applied and USD 350 remains open. If a processor shows a USD 590 net deposit for a USD 600 charge, require the fee/charge linkage before reconciling the USD 10 difference.

Review the table against originals and recalculate totals. Keep unresolved differences visible. For follow-up drafts use `invoice-follow-up`; for projected cash use `cash-flow-planning`. These routes do not authorize sending or moving money.

For a new or updated invoice, route to `invoice-preparation`. Compare invoice rates, scope changes, credits/deposits and due-date rules with the private [agreed terms record](../../references/engagement-terms-record.md); unresolved terms remain exceptions, not silently assumed agreements.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Business Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
