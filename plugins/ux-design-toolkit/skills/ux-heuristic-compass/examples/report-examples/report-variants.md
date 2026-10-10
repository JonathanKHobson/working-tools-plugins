# UXHC Report Variant Examples

These are example shapes the renderer must support. The canonical visual
baseline is the approved AI-only v2 report structure.

## Compact Report

- 10 core heuristics.
- No optional profiles.
- No HIL note.
- Short evidence appendix.

## Full 14-Heuristic Report

- H01-H14 active.
- Optional profile labels appear through heuristic names and scope metadata.
- Scorecard grid grows without changing section order.

## Omitted Profile Report

- Core plus one optional profile.
- Audit Scope and Omitted Profiles section names the missing optionals and
  rerun guidance.

## HIL-Calibrated Report

- Same AI-first structure.
- HIL note appears only from `hil_compliance` or answered gate data.

## Evidence-Limited Report

- Evidence Limits section moves before the roadmap.
- Findings with low confidence remain framed as hypotheses to validate.
