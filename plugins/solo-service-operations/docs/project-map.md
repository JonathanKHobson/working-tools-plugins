# Solo Service Operations Studio project map

Purpose: source-backed solo-service invoice administration, payment matching and cash visibility. This distinct financial-record lane follows Marketing's agreed offer and Work Management's delivery scope; it does not duplicate either owner.

- `.codex-plugin/plugin.json`: native identity; four focused skill entrypoints.
- `skills/invoice-preparation/`: agreed terms, work evidence, recipient-owned client routing and verified document creation.
- `skills/invoice-follow-up/`: current receivables and draft/sent boundaries.
- `skills/payment-reconciliation/`: invoice allocations and explained differences.
- `skills/cash-flow-planning/`: dated cash model, source coverage and scenarios.
- `references/`: shared source/data boundaries, agreed terms, work evidence, existing client workflow routing and explicit allocation input.
- `scripts/reconcile.py`: local JSON-in/stdout-out exact-decimal checker; no network, persistence or transactions.
- `tests/test_reconcile.py`: synthetic allocation/error behavior checks.
- `libraries/`: inactive pinned upstream methods/support, licenses and notices.
- `docs/provenance.md`: adaptation decisions and source hashes.

Verification: `python3 -B -m unittest discover -s tests -v` from this root, skill-creator validation, Master Security Toolkit scan/manual review, native install and parity. No accounts or private records live here. Live source reconciliation is distinct from synthetic checks. Next changes belong to the relevant existing workflow; connectors and additional financial domains require separate demonstrated need and review.
