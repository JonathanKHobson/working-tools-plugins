---
name: oppia-usability-testing
description: Design moderated or unmoderated Oppia usability tests for real tasks, flows, prototypes, and critical user journeys. Use when the team needs to observe whether a target user can understand or complete an Oppia goal. Do not use for expert-only interface inspection; route that to Oppia heuristic evaluation.
---

# Oppia Usability Testing

## Overview

Turn an Oppia decision and CUJ into observable tasks, neutral moderation, useful
measures, and a bounded findings plan. Search prior usability evidence first.

Source anchors: `drive.oppia.usability-script.v1`,
`drive.oppia.research-plan-obsolete.v1`, and
`drive.oppia.cuj-web-v3.v1`. Cross-cutting quality rules are adapted from
`external.ux-research-skill.v1.0.0`.

## Workflow

1. State the decision, target persona, CUJ or flow, device/context, and product
   state being tested.
2. Search Oppia evidence for known friction, past tests, and participant
   constraints. Do not retest a settled issue without a change hypothesis.
3. Choose moderated or unmoderated based on access, risk, prototype fidelity,
   and the need for probing. State what this mode cannot establish alone.
4. Justify sample coverage from the intended claim, relevant persona/context
   variation, decision risk, evidence depth, and an iterative stopping rule.
   Never substitute a universal participant count.
5. Define realistic scenarios and one goal-oriented task at a time. Avoid
   exposing interface labels or the intended path in task wording.
6. Define observations before metrics:
   - first action and route;
   - success, partial success, failure, or abandonment;
   - hesitations, backtracks, errors, help, and moderator intervention;
   - comprehension, confidence, and notable quotes;
   - device, accessibility, language, and connectivity constraints.
7. Add participant protection: consent, recording permission, safe test data,
   and stop points before personal, payment, or account-sensitive actions.
8. Plan relevant assistive technologies, accommodations, language or
   interpretation, device, bandwidth, age, and power conditions as part of the
   study design.
9. Write neutral think-aloud prompts and silence nudges. Do not teach the task.
10. Pilot the complete experience: invitation, consent, task interpretation,
    accommodations, links/states, timing, evidence capture, analysis, fallback,
    closing, and storage. Version substantive changes and decide whether pilot
    or pre-change evidence remains comparable.
11. Synthesize patterns with denominators and counterexamples; separate observed
    behavior from post-test opinion. Examine conflicting outcomes by persona,
    context, version, assistance, and protocol deviation.
12. If AI assists coding or synthesis, use permitted minimized data, preserve
    source IDs, test a human-reviewed subset, and disclose material use.

## Output Contract

- research question and decision;
- participant criteria and sample rationale;
- environment and mode;
- scenarios and verbatim tasks;
- success criteria, observations, and optional measures;
- moderation, consent, recording, and safety script;
- session logistics and fallback plan;
- analysis matrix, limitations, and stop condition.
- sample rationale, pilot/change log, inclusion coverage, and AI-assistance
  status where applicable.

## Stop Conditions

- Do not test a flow that is too incomplete to answer the question.
- Stop before participants enter real sensitive data or perform irreversible
  actions.
- Do not add tasks that are unrelated to the chosen decision.

## Verification

- Task wording describes a goal, not a sequence of clicks.
- Success can be observed consistently across sessions.
- Moderator interventions are defined and recorded.
- CUJ, persona, device, and accessibility context are explicit.
- Findings preserve participant count and do not overgeneralize.
- The sample rationale states required variation and a stopping rule.
- Pilot data are analyzable and protocol changes are versioned.
- Negative cases and contradictory behavior remain visible.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UX Researcher. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
