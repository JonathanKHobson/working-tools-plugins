# Portfolio Crafter Agent Roles

These files are prompt-role guidance for a host AI. They are not executable agents.

Use them when a portfolio task needs focused review:

- `portfolio-strategist.md`: reader, format, case selection, and portfolio narrative.
- `case-study-writer.md`: full case-study drafting and rewrite.
- `artifact-caption-editor.md`: captions, alt text, and artifact proof.
- `evidence-integrity-reviewer.md`: unsupported claim, ownership, and metric checks.
- `confidentiality-auditor.md`: redaction, sensitivity, and share-readiness.
- `buyer-proof-strategist.md`: buyer risk, proof hierarchy, trust path, and case selection.
- `service-offer-case-advisor.md`: service-aligned case cards and offer proof.
- `portfolio-site-planner.md`: website proof planning only when explicitly requested.
- `portfolio-assessment-coach.md`: competency evidence maps, reviewer simulation, scaffolded practice, and special-context support.
- `portfolio-transfer-strategist.md`: visitor journey, core loop of trust, interaction usefulness, accessibility, and gimmick risk.

## Coordination Pattern

For contractor-facing proof:

1. Buyer Proof Strategist chooses the buyer risk, proof hierarchy, and strongest case.
2. Service Offer Case Advisor maps proof to the service or offer.
3. Evidence Integrity Reviewer blocks unsupported claims, metrics, or testimonials.
4. Confidentiality Auditor checks publishability before any public-facing use.

For explicit website planning:

1. Portfolio Site Planner confirms the website request and maps proof before design.
2. Buyer Proof Strategist checks the five-minute reader path.
3. Confidentiality Auditor flags private artifacts, names, metrics, and screenshots.

For competency or reviewer-readiness work:

1. Portfolio Assessment Coach maps competencies, reviewer decision, evidence, and gaps.
2. Portfolio Strategist chooses case order and reader speed.
3. Evidence Integrity Reviewer blocks unsupported claims or invented metrics.
4. Confidentiality Auditor checks redaction before anything becomes share-facing.

For game-design transfer or interactive portfolio review:

1. Portfolio Transfer Strategist maps the visitor journey and core loop of trust.
2. Evidence Integrity Reviewer blocks unsupported game-design, playtest, metric, or shipped-experience claims.
3. Confidentiality Auditor checks proof, artifacts, and screenshots before share-facing use.
4. Portfolio Strategist turns the findings into case order, captions, or reader-path revisions.

## Handoff Rule

Each role should preserve visible gaps. Do not turn `[MISSING INFO: ...]` into polished claims.
