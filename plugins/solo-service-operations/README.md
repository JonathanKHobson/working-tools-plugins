# Solo Service Operations Studio

Prepare evidence-backed invoices, draft proportionate follow-ups, reconcile settled payments and plan dated cash flow from supplied private records.

## Start with a real task

| Ask | Bring | You receive |
| --- | --- | --- |
| “Prepare a review copy of this month’s invoice from the agreed terms and work evidence.” | Terms, period and dated work records | Reconciled invoice with unresolved items visible |
| “Match these invoice and payment exports as of today.” | Invoice register, settled payments and cutoff | Allocation table and unexplained differences |
| “Show the next 60 days of cash timing if this receivable is delayed.” | Opening cash, dated inflows and obligations | Scenario with minimum balance and assumptions |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/invoice-preparation/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Choose the matching focused skill in the table. Invoice-preparation answers broad getting-started questions here; use follow-up, reconciliation or cash-flow directly when that is the requested outcome.

| Task / skill | What it produces |
| --- | --- |
| [cash-flow-planning](skills/cash-flow-planning/SKILL.md) | Build a source-backed cash-flow snapshot for solo-service work from supplied balances, receivables and obligations, with explicit scenarios and missing-data limits. |
| [invoice-follow-up](skills/invoice-follow-up/SKILL.md) | Review verified solo-service receivables and prepare accurate, proportionate invoice follow-up drafts. |
| [invoice-preparation](skills/invoice-preparation/SKILL.md) | Prepare or update evidence-backed solo-service invoices, using agreed terms, active-human-work evidence and a supplied document template. |
| [payment-reconciliation](skills/payment-reconciliation/SKILL.md) | Reconcile solo-service invoices against supplied settled-payment records, explain discrepancies and retain source evidence. |

## Availability and recovery

This package has no `.mcp.json`, account connector, daemon or payment action. It works from authorized supplied/private-project records and an optional local read-only reconciliation helper. Verify source coverage and settlement before asserting what is owed or paid; an invoice draft is not sent, and an unmatched payment is not a confirmed balance. If data is missing, deliver the supported partial analysis and name the smallest required record.

See [project map](docs/project-map.md) and [provenance](docs/provenance.md) for maintenance and source boundaries. Client records stay outside this package. Edit canonical source, validate/review, reinstall through the native manager and verify file parity; installed does not mean current data or account access.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Run the local sample

Read [installation](docs/installation.md). Python 3.9+ is enough for the dependency-free allocation helper and synthetic tests:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/reconcile.py examples/reconciliation-input.json
```

The fictional sample allocates USD 250 of a USD 600 invoice and leaves USD 350 partial. A pending payment is excluded. The helper reads input and prints JSON; it never modifies the file, authenticates a bank, posts an entry, sends a reminder or moves money. Inspect the supplied records before applying conclusions to real accounts.

Original public adaptation/helper contributions are Apache-2.0, copyright Jonathan Kyle Hobson. Retained upstream procedures and role-source notices preserve their own terms; see [third-party notices](THIRD_PARTY_NOTICES.md). No personal client record, invoice design or account connector is included.
