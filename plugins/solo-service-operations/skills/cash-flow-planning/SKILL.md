---
name: cash-flow-planning
description: Build a source-backed cash-flow snapshot for solo-service work from supplied balances, receivables and obligations, with explicit scenarios and missing-data limits. Use for near-term cash timing; no payments, investment decisions or automatic accounting connections.
---

# Cash-flow Planning

Show what cash may be available, when, and which assumptions matter. Read [source/data boundaries](../../references/source-and-data-boundaries.md). Use existing spreadsheet tools for an editable workbook when requested. No new connector, paid service or scheduler is required.

## Define inputs and coverage

Choose the relevant horizon (a dated weekly view for a near-term question; 30/60/90-day buckets when useful), business entity/accounts, currency and as-of date. Obtain a sourced opening **available cash** balance and distinguish restricted funds, credit limits and receivables. With no opening balance, deliver **net change only**; do not claim ending cash or runway.

Inventory dated inflows and outflows with source IDs, amounts/currency, settlement date or expected date, status and assumptions. Include invoiced work, documented scheduled payments, agreed bills/subscriptions, known fees and supplied obligations. A sales lead or unsigned proposal is not a committed receivable. Do not estimate taxes, invent payment timing or infer future payroll from an old transaction without labeling a user-approved assumption.

Use one source of record per event. An invoice, processor charge, payout and bank deposit may describe stages of the same cash event. Match them or label uncertainty rather than add them. Model net settlement and separately account for documented fees without double counting. Identify whether payments through the as-of cutoff are already included in opening cash; exclude them from future flows. Keep currencies separate unless an explicit dated conversion policy is supplied.

## Build an auditable model

1. Mark actual settled cash, confirmed scheduled items, expected dated items and uncertain opportunities distinctly. Explain coverage and unconfirmed amounts before presenting totals.
2. For each bucket and currency: `closing cash = opening cash + inflows - outflows`. Carry closing cash to the next bucket. Do not add cumulative 30/60/90 figures together. Show the next known large obligation at its actual date; a monthly net total can hide a mid-month shortage.
3. Use observed settlement history only when representative. Report sample size, date range, whether lag is from issue date or due date, and exceptional cases. With sparse data, retain agreed due dates and disclose uncertainty; do not manufacture statistical confidence bands.
4. Produce an expected scenario and a named delay/downside scenario when uncertainty affects the answer. For example, shift one identified receivable by a user-supplied two weeks. Label this a scenario, not a probability or confidence interval. Show the input delta and resulting minimum balance/date. Do not assign an arbitrary ±30% band from a small sample.
5. Flag incomplete accounts, disputed receivables, pending/reversed payments, timing concentrations and negative projected balances. A negative projection is an assumption-dependent warning, not proof of insolvency or advice to borrow.

## Worked example (fictional)

Opening available cash on October 1: USD 1,000, sourced from a statement. October 10 expected invoice receipt: USD 600; October 15 documented obligation: USD 900. Expected closing cash: USD 700. If the receipt arrives October 24 instead, cash immediately after October 15 is USD 100, then USD 700 on October 24. Both month-end figures are the same; the timing risk differs. An unaccepted USD 500 proposal is excluded from the base and may appear separately as an opportunity, never confirmed cash.

## Deliver and verify

Return scope/as-of date, source coverage, opening balance or net-change-only warning, dated ledger, per-currency bucket summary, assumptions, scenarios and the smallest next verification. If a workbook is requested, keep raw/source data, assumptions and formula-driven projection distinct; verify formulas and rendered output through the spreadsheet owner. For a simple request, a concise table is sufficient.

Check date cutoffs, signs, bucket membership, opening-balance double counts, cross-source duplicates, net/gross fees and currency before claiming accuracy. Recalculate at least one bucket independently. Show unresolved gaps. This skill supplies cash-record analysis; financing, investment, tax and legal advice require their own current sources and qualified judgment. It does not create transactions, contact clients, adjust invoices or enroll a recurring forecast.

For a specific record discrepancy use `payment-reconciliation`; for an authorized reminder request use `invoice-follow-up`. See [source provenance](../../docs/provenance.md) for retained upstream material and adaptation decisions.

For a new or updated invoice, route to `invoice-preparation`. Compare invoice rates, scope changes, credits/deposits and due-date rules with the private [agreed terms record](../../references/engagement-terms-record.md); unresolved terms remain exceptions, not silently assumed agreements.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Business Operations Specialist, Business Advisor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
