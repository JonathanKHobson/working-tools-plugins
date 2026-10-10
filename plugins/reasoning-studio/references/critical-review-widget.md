# Critical Review widget

For deliberate human inspection of a completed Critical Compass content or paper assessment. One review family; not a new scoring or audit route.

Use `critical_create_review` with explicitly supplied completed audit_data and/or validated anchored_cards, title and source_revision. Anchored cards are {reviewer, snapshot}; supply the exact extracted source_text and source_id SHA256 for source checks. No arbitrary paths, URL fetching, scoring, gate resolution or analyst execution. Legacy audit input currently supports the full five-dimension council schema; unsupported quick scans fail closed. Anchored-only reviews are supported without a legacy report.

Use `critical_open_review` with the returned snapshot_id only when the human wants the interactive view. `critical_read_review` reads the same immutable analysis without UI. Import is private, content-addressed and idempotent for identical input. Up to 2 MB input/output. Source payloads are not edited. Imported source metadata is caller-supplied; a hash validates consistency, not external authenticity.

The UI keeps each method/reviewer separate; it cannot treat legacy or experimental scores as calibrated truth. Unknown criteria withhold totals. Exact excerpts, reference-only locators, and mismatched page references remain distinct. Supplied synthetic human responses remain visibly separate from actual user input. Do not assume model perspectives are human participants or independent empirical corroboration.

Criteria marks and question drafts are view-local and clear on review switching or close. Discuss sends an explicit selected-criteria packet if supported; otherwise it prepares copyable text and says it was not sent. Host acknowledgment does not prove an assistant response. No automatic persistence, rescoring or gate completion occurs. Existing full-audit consent/HIL instructions remain authoritative.

Runtime is bound through an operator-selected Critical Review JSON binding; the launcher does not install dependencies or repair missing mounts. Native installation and actual rendered host acceptance are separate evidence.
