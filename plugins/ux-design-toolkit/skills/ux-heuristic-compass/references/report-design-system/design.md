# UXHC Report Design System

This is the North Star for UXHC generated reports. The MCP renderer owns the
HTML. The host AI supplies or repairs bounded content slots, then retries
`validate_ux_report_payload` and `generate_ux_audit_report`.

## Non-Negotiables

- One page only.
- Static HTML only: no scripts, links, external assets, imports, or CSS asset URLs.
- AI-only audit language by default.
- HIL language appears only when the payload records HIL usage.
- Human-panel or blended-score language appears only when explicit human-panel data exists.
- Scorecard, plain-language read, top finding, and recommendations lead before support flows.
- Evidence refs, paths, and source labels render as plain text.
- If validation blocks, repair the payload. Do not create handmade HTML or PDF outside UXHC.

## Section Order

1. Header and audit metadata.
2. Mission context.
3. Overall grade and Plain Language Read.
4. Next Research Recommendation.
5. Before using this interface warning.
6. Critical/top finding.
7. Heuristic scorecard.
8. Prioritized findings.
9. What is working well.
10. Evidence limits.
11. Recommended next validation steps.
12. Prioritized fix roadmap.
13. High-impact / low-effort micro-solutions.
14. Audit scope and omitted profiles when present.
15. Complete checklist scores.
16. Evidence appendix.

## Product Boundary

The report is a UX heuristic audit deliverable. It can include Atlas-adapted
support flows, teaching activities, HIL notes, and agent-mode context, but those
support layers must never become the center of the artifact.
