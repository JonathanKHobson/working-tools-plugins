---
name: oppia-heuristic-evaluation
description: Plan, conduct, and synthesize Oppia heuristic evaluations for a defined persona, critical user journey, device, and release slice. Use for expert or trained-volunteer inspection of interface risks and severity. Do not present heuristic findings as observed participant behavior.
---

# Oppia Heuristic Evaluation

## Overview

Use a consistent expert-review method while preserving evaluator independence
and evidence. The spreadsheet is structure, not the goal; actionable findings
are the goal.

Source anchors: `drive.oppia.heuristic-onboarding.v1` and
`drive.oppia.cuj-web-v3.v1`. Method-limit, inclusion, counterevidence, and
AI-assistance rules are adapted from `external.ux-research-skill.v1.0.0`.

## Workflow

1. Define persona, CUJ, device, account state, language, connectivity mode,
   environment, and release slice.
2. Search historical Oppia evidence so evaluators understand known risks without
   copying old conclusions into the current review.
3. Choose a cycle:
   - rapid: narrow surface, 1-2 evaluators, fast directional output;
   - thorough: full high-value journey, 3-5 independent evaluators, synthesis
     and prioritization.
4. Use Nielsen's ten heuristics as the core set. Add only relevant Oppia lenses,
   such as accessibility, inclusion, journey continuity, satisfaction, or UX
   writing/tone.
5. Define relevant disability/access needs, assistive technologies, language,
   device, bandwidth, age, and evaluator-knowledge assumptions. A deterministic
   accessibility failure can be severe even when observed once.
6. Have evaluators review independently before seeing others' scores.
7. For each issue, capture page/moment, heuristic, observed interface evidence,
   affected user goal, severity, rationale, and possible improvement.
8. Use the Oppia severity scale:
   - 0: passed or no meaningful issue;
   - 1: cosmetic;
   - 2: minor;
   - 3: major;
   - 4: catastrophic or urgent.
9. Mark non-applicable checks explicitly. Do not force every heuristic onto
   every screen.
10. Synthesize agreements, meaningful score differences, repeated patterns,
   quick wins, larger opportunities, and questions requiring user research.
11. If AI assists clustering or reporting, keep evaluator records and page
    evidence as the sources, verify the synthesis manually, and disclose
    material use.

## Output Contract

- scope and cycle choice;
- evaluator instructions and lens set;
- independent finding records with evidence and severity;
- synthesis clusters and score disagreements;
- prioritized quick wins, bigger changes, and follow-up research questions;
- limitations and stop condition.
- assumed user/context coverage and AI-assistance status where applicable.

## Stop Conditions

- Stop a finding at expert evidence; do not invent user impact as observed fact.
- Route behavioral uncertainty to usability testing.
- Do not expand a rapid cycle into a full-site audit.

## Verification

- Persona, journey, device, and state are explicit.
- Each issue identifies where it occurred and why it matters.
- Severity is supported by impact, frequency expectation, and recoverability.
- Independent observations remain visible through synthesis.
- Recommendations are proportional to evidence and scope.
- Expert predictions are not reported as participant evidence; consequential
  uncertainty is routed to direct research.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Design Quality Reviewer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
