---
name: oppia-persona-research
description: Identify, validate, revise, and confidence-rate Oppia personas from research evidence. Use when the team needs to define meaningful user groups, assess whether an existing persona is supported, or turn cross-study behavioral patterns into a working persona. Do not invent demographic detail or treat a persona as a fictional profile.
---

# Oppia Persona Research

## Overview

Treat personas as evidence-backed models of goals, behaviors, constraints, and
decision contexts. Oppia's corpus, interviews, and observed behavior lead;
netnography and stakeholder knowledge may triangulate but not silently fill
gaps.

Source anchors: `drive.oppia.persona-handoff.v1` and
`drive.oppia.research-synthesis.v1`. Evidence-chain, inclusion, negative-case,
and AI-assistance rules are adapted from
`external.ux-research-skill.v1.0.0`.

## Workflow

1. State why a persona distinction matters to an Oppia decision or CUJ.
2. Browse Oppia interview/persona records and search the full corpus for the
   candidate group's goals, pathways, behaviors, constraints, and friction.
   Check whether original consent, access, population, context, product
   version, and timing permit the proposed secondary use.
3. Build an evidence table with evidence ID, user/context, direct behavior or
   reported belief, interpretation, and confidence.
4. Cluster meaningful behavioral differences. Do not split groups merely by
   age, country, job title, or another demographic unless it changes needs or
   behavior.
5. Test alternative explanations and negative cases.
6. Audit evidence coverage and source concentration across language,
   disability/access needs, device, infrastructure, geography, age, and power
   conditions that could change the behavior model.
7. Assign a status:
   - `confirmed`: repeated direct evidence across relevant sources;
   - `directional`: some direct evidence, meaningful gaps remain;
   - `provisional`: mostly indirect, contextual, or single-source evidence;
   - `unsupported`: no adequate evidence for the claimed persona.
8. Compare the evidence with the current persona. Preserve confirmed elements,
   revise contradicted assumptions, and label new hypotheses.
9. Link the persona to specific Oppia goals/CUJs and the product implications
   the evidence actually supports.
10. If AI assists clustering or synthesis, use permitted minimized evidence,
    retain source IDs, test omissions and minority patterns against a
    human-reviewed subset, and disclose material use.

## Output Contract

- decision purpose;
- persona label and behavioral basis;
- goals, context, discovery pathway, constraints, needs, and blockers;
- evidence table with stable IDs;
- confirmed elements, revised assumptions, and hypotheses;
- confidence status and coverage gaps;
- contradictory cases, alternative explanations, and source concentration;
- CUJ/product implications;
- next research needed, only when decision-relevant.

## Stop Conditions

- Do not add decorative biography, a stock-photo identity, or precise personal
  details that are not evidenced.
- Do not merge distinct behavioral patterns for visual simplicity.
- Do not create a new persona when a segment note or scenario is sufficient.

## Verification

- Every asserted behavior maps to evidence or is labeled as a hypothesis.
- Confidence reflects source quality, independence, and coverage.
- Contradictory cases are visible.
- Geography is treated as context, not destiny.
- Persona changes are expressed as a bounded current/proposed diff.
- Generated clusters are never treated as source evidence and remain subject
  to accountable human review.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UX Researcher. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
