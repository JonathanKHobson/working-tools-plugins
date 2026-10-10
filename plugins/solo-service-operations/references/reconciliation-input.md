# Explicit allocation input

The helper accepts one JSON object with `as_of` (ISO date), `invoices` and `payments`. All monetary amounts are positive decimal **strings**; currency is an uppercase three-letter code. IDs must be unique within invoices/payments. Input is normalized evidence, not an arbitrary bank export.

Invoice fields: `invoice_id`, `customer_id`, `currency`, `amount`, `source_ref`. `amount` must be the payable basis selected for this reconciliation. If using an open balance, include only payments not already deducted from it. Exclude void/draft/disputed records from this supported subset and report them separately.

Payment fields: `payment_id`, `customer_id`, `currency`, `amount`, `source_ref`, `status` (`settled`, `pending`, `failed` or `reversed`), `settled_on` for settled records, and optional `allocations`: objects with `invoice_id` and `amount`. A settled payment lacking allocations remains unapplied. Future-settled and nonsettled records are not applied. Duplicate allocations or allocation sums greater than the payment are input errors.

```json
{
  "as_of": "2026-10-01",
  "invoices": [{"invoice_id":"I1","customer_id":"C1","currency":"USD","amount":"600.00","source_ref":"fictional-invoice:1"}],
  "payments": [{"payment_id":"P1","customer_id":"C1","currency":"USD","amount":"250.00","status":"settled","settled_on":"2026-09-30","source_ref":"fictional-bank:4","allocations":[{"invoice_id":"I1","amount":"250.00"}]}]
}
```

Expected: I1 is `partial`, USD 250.00 allocated, USD 350.00 remaining. Unknown invoice/client/currency allocations are reported and not applied. For each payment `total_unapplied` includes those amounts; do not sum it with its reason-detail rows. The output has no mixed-currency totals. Negative remaining means overpaid in these records; it does not authorize a refund.

The helper does not deduplicate alternate exports with different IDs, interpret processor fees, model refunds/reversals, check source completeness, authenticate payments or infer customer identity. Do those checks before preparing input; a synthetic passing case cannot prove a real invoice paid.

Every exception has `additive: false`: detail rows overlap and must never be summed. `unapplied_settled_by_currency` is the non-overlapping total of unallocated eligible settled payments, separated by currency. It excludes pending/failed/reversed and after-cutoff payments, and is not a bank balance or cash forecast. Use an actual evidence cutoff; future plans are not settled receipts.
