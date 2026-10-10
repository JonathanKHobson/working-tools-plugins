# Component Rules

## Header

Shows report title, compact audit metadata, generated date, harness version, and
overall grade badge.

## Overall Grade Card

Compact, content-sized, and top-aligned with the Plain Language Read card. Never
stretch to match the longer text card.

## Plain Language Read

Contains the short read, Next Research Recommendation, and the required
`Before using this interface,` warning.

## Heuristic Score Item

Shows grade, percentage, average severity, heuristic name, and descriptor.
Render one item per active heuristic.

## Finding Card

Shows rank, severity badge, heuristic/checklist ID, observed issue,
recommendation, impact note, evidence ref, and confidence.

## Checklist Details

Use static `<details>` groups by heuristic. Show every row. Do not use JavaScript
filters.

## Evidence Appendix

Render evidence refs, source labels, screenshot paths, and metadata paths as
plain text.
