# Human-systems decisions

Use this reference when a review or design finding depends on how people perceive, remember, decide, act, recover from errors or carry workload. It turns named laws and effects into conditional decisions. When an inherited playbook states a fixed number, such as a maximum option count, a 44-pixel design target mislabelled as the WCAG AA minimum or a count-based cognitive-load score, use this reference for the decision and [verification](verification.md) for current accessibility criteria. Normative accessibility floors always apply. A reviewer's application of these decisions produces hypotheses, not participant evidence.

## Pointing: only for repeated rapid aimed movement

Fitts' law predicts movement time from distance and target width for rapid aimed pointing. It doesn't model finding, reading or deciding. First confirm the problem is acquisition: people already know the target and repeatedly miss it or take too long moving to it. Then enlarge the hit area, shorten the distance from the preceding action, and separate destructive targets from frequent benign ones. Meet the WCAG 2.2 target-size floor or its spacing exception, and move toward the enhanced size when the audience or input mode needs it. Provide a non-drag alternative for dragging and a keyboard path for repeated expert actions. Evaluate time and errors separately. Don't cite Fitts' law to make a marketing button bigger or to justify a universal size.

## Memory: count what is carried, not what is visible

Working-memory limits concern information held in mind, measured when rehearsal and grouping are prevented. Visible options are recognition, not recall. Count **carried items**: anything the person must remember across a screen change, scroll, tab, step or interruption in order to act or compare. Reduce them by co-locating the things compared (same units and scales), echoing selection and scope beside results, labelling directly instead of through distant legends, and keeping status visible. Group long visible lists by the person's vocabulary and make them searchable. Hide only genuinely rare options, because hiding a frequent option turns recognition into recall. Offer keyboard commands as an additional path for experts, not a replacement.

## Before and after an action: route existing consequence guidance

Start with [UX writing](ux-writing.md), which already requires stating destructive or consequential effects before confirmation. For each consequential or non-obvious action, check the **feedforward**: what will change, where and by how much, before commit. For example: "Scenario: capacity 30 → 40, source unchanged." Give **feedback** where the person is looking, distinguish pending, success and failure, and expose status messages to assistive technology without moving focus. Check that control direction, position and grouping map onto the displayed effect. A preview that differs from the result is worse than no preview. Affordances or signifiers say *that* something can be done; feedforward says *what it will do*. The engineering open-loop analogy is only a design prompt: when an action's result is hard to observe, test whether feedback makes it clear. MathWorks X13 supports the engineering term, not the UI outcome.

## Interruption: state plus a resumption cue

Preserving state keeps the data; a cue restores the person's intention. For multi-step or long-running work, record the last completed step, the pending intention visible in state (such as the next unreviewed item), and any unsaved values *as focus changes*, so the cue already exists when the interruption comes. On return, show the cue where work resumes, list pending changes, and offer continue, review or discard with their consequences stated. Keep drafts and scenarios visibly separate from committed data, and never silently restore hypothetical values. Warn before timeouts that lose data, allow extension, and return to the same state after re-authentication. On shared devices, hide draft details until the person has authenticated. The interrupted and stale checks in [interaction resilience](interaction-resilience.md) still apply to system integrity.

## Consequential actions: use the existing risk matrix

Use [frontend-design-premium's confirmation-strength matrix](../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md) for the choice among no confirmation with optional Undo, confirmation or Undo for recoverable destruction, and stronger app-owned confirmation for irreversible, external, financial or catastrophic effects. For predictable input errors, also use constraints, defaults and inline validation that preserves input. This reference adds the task check: name the object, scope and downstream effect before a consequential commit, and verify the promised recovery really works.

Don't add a generic confirmation to frequent reversible actions, offer undo the backend can't honor, or use confirm-shaming copy. Where WCAG 3.3.4 applies (legal, financial, data modification, test responses), at least one of reversible, checked or confirmed is required.

## Workload is multidimensional, not "less is better"

Workload includes mental, physical and temporal demand, frustration, effort and perceived performance, and it can diverge from performance. Before recommending "simplify", name the dimension at risk and the duration of use. Monitoring and glance surfaces need ambient scope, freshness and coverage context, so that an empty result can be trusted. Learning or reflective tasks may deliberately keep effort that builds understanding while removing extraneous effort. Time-pressured tasks benefit from moving effort out of the critical moment. Every "simplify" recommendation says what moved and where. Workload is only measured by participants rating or performing real tasks; a reviewer can only hypothesize it.

## Emotion: observed, self-reported or inferred

Record every emotion statement as exactly one of: observed behavior, with its interpretation in a separate field; the participant's own words or rating; or a reviewer inference with an alternative explanation and a test. Facial movement isn't a reliable indicator of a specific emotion, and screenshots support only inference. Turn inferred emotion into a design question or a research task, not a finding. Don't use emotional inferences to target persuasion.

## Optional PCEA task worksheet

For task analysis or test preparation, the PCEA lens can be used: Perception, Cognition, Emotion, Action. It was proposed by Kyle Hobson as an extension of the PCA framing, and it is an attributed candidate lens, not a validated method. Use one row per step, with these columns:

- Perception
- Cognition, marking carried items and recognition vs. recall
- Emotion observed
- Emotion self-reported
- Emotion inferred, with an alternative and a test
- Action, covering control, motor demand and keyboard path
- Feedforward / feedback
- Error / recovery
- Workload / context
- Evidence type (inspection, rendered check, participant, analytics)

Leave cells empty rather than inventing content.

## Checks

For a finding that cites this reference, state the card-level condition that triggered it, the evidence type, what would change the judgment, and the check you ran or couldn't run. Report pointing changes with time and errors separately, memory changes as a before/after carried-item count, feedforward by whether each consequential action states its consequence, resumption with a forced interruption, and consequential actions by mapping each to the existing confirmation-strength matrix.

## Provenance and scope

This is a local synthesis from the 02 human-systems research packet (2026-09-29). Sources: Soukoreff & MacKenzie 2004 (Fitts' law scope); WCAG 2.2 and Understanding 2.5.8; Cowan 2010 (working memory); Nielsen's ten heuristics; Zhang & Norman 1994 (external representations); Vermeulen et al. 2013 (feedforward); Altmann & Trafton 2002 (goal resumption cues); Hart 2006 (NASA-TLX); MathWorks R2026b (engineering terminology only); Barrett et al. 2019 (emotion inference). The PCEA lens and the H11–H13 heuristic extensions are Kyle Hobson's proposals from HSE 521 coursework. This is research-backed decision guidance, not validated performance claims. No third-party text is reproduced.

## Read the complete task-matching card

The overview above is an orientation, not a replacement for the full evidence, competing considerations and cases. Select only the relevant method:

- [target acquisition](human-systems/target-acquisition.md)
- [carried memory](human-systems/carried-memory.md)
- [action feedback](human-systems/action-feedback.md)
- [task resumption](human-systems/task-resumption.md)
- [consequential error](human-systems/consequential-error.md)
- [workload tradeoffs](human-systems/workload-tradeoffs.md)
- [emotion evidence](human-systems/emotion-evidence.md)
- [optional heuristic observations](human-systems/optional-heuristic-observations.md)

PCEA remains Kyle Hobson’s optional attributed proposal. Preserve the unresolved PCA/PCEA and Material/Mental wording in source notes; do not silently present either expansion as a validated standard. No glossary renaming or MCP rubric-count change is part of this update.
