---
name: oppia-cuj-research
description: Define, audit, and revise evidence-backed Oppia critical user journeys (CUJs). Use when the team needs to map an end-to-end user goal, assess journey coverage or health, align research with acceptance tests and metrics, or propose a bounded CUJ change. Do not rewrite the full CUJ system for a single research question.
---

# Oppia Critical User Journey Research

## Overview

Connect a meaningful user goal to sequential steps, expectations, risks,
research evidence, and cross-team verification. A CUJ is an end-to-end goal
narrative, not a feature inventory or sitemap.

Source anchors: `drive.oppia.cuj-web-v3.v1`,
`drive.oppia.persona-handoff.v1`, and
`drive.oppia.research-synthesis.v1`. Evidence-chain, inclusion,
counterevidence, and AI-assistance rules are adapted from
`external.ux-research-skill.v1.0.0`.

## Workflow

1. Define the user type/persona, goal, start state, success state, and why the
   journey is critical.
2. Search Oppia evidence for actual discovery pathways, constraints, failure
   points, workarounds, success signals, and negative cases. Record population,
   context, product version/date, and whether old evidence transfers to the
   current journey.
3. Inspect the current CUJ when available. Preserve its identifier and lower-is-
   higher importance convention.
4. Write a continuous narrative. Each step should include user intent/action,
   system response, expected state, and evidence or assumption status.
5. Check variants that materially change the journey: signed-in state, device,
   keyboard/screen reader, language, slow connectivity, and cross-site handoff.
6. Map known risks and evidence gaps to the step they affect.
7. Connect the journey to the appropriate owner surfaces:
   - acceptance tests and screenshots;
   - UX/design reference states;
   - product metrics and monitoring;
   - UXR baseline or follow-up studies;
   - issue labels and journey-health reporting.
8. For changes, produce current state, proposed end state, and a bounded diff.
   Distinguish research evidence from product policy.
9. If AI assists mapping or synthesis, retain the underlying evidence and step
   IDs, test omissions and alternative paths manually, and disclose material
   use.

## Output Contract

- CUJ identifier, importance, persona, goal, start, and success state;
- sequential step table with expectations and evidence status;
- device/accessibility/language/network variants;
- risk and gap map;
- research, acceptance-test, design, metric, and issue-link requirements;
- current/proposed diff when revising;
- limitations, owners, and next verification.
- evidence freshness, counterpaths, and AI-assistance status where applicable.

## Stop Conditions

- Do not add low-value feature coverage that does not serve the named goal.
- Do not silently renumber or replace other CUJs.
- Do not claim a path is validated when steps are based on assumptions or
  stakeholder intent.
- Stop at a proposal when cross-team approval or production verification is
  required.

## Verification

- Reading steps top to bottom produces an unbroken goal narrative.
- Every critical expectation has evidence, a test, a metric, or an explicit gap.
- Variants are relevant rather than exhaustive checkbox coverage.
- The proposed diff is traceable and limited to the requested journey.
- Research findings are not confused with acceptance-test status.
- Contradictory paths or segment differences remain visible instead of being
  averaged into one idealized journey.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UX Researcher. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
