# UXHC Evaluator Bias Guard

UX heuristic audits can be distorted by the evaluator's own expectations. Use this guide before accepting high-severity findings, surprisingly clean scores, or findings based on thin evidence.

This guide adapts the useful intent of `patterns:heuristics-biases-preflight` and `patterns:cognitive-debiasing` into UXHC audit practice.

## Fast Bias Preflight

Before finalizing the audit, ask:

1. Did I rate visual polish before task success?
2. Did the first screen anchor the rest of the audit?
3. Did I look hardest for the issue I expected to find?
4. Did familiarity with the product make the interface feel easier than it is?
5. Did unfamiliar conventions look wrong only because they are unfamiliar to me?
6. Did audience context justify severity, or am I filling in missing evidence?

If the answer is yes or uncertain, lower confidence or route the finding to `stress_test_heuristic_finding`.

## Common UXHC Biases

| Bias | Audit risk | Guard |
| --- | --- | --- |
| Aesthetic bias | beautiful screens get gentler ratings | score functional heuristics before H8 polish |
| Halo effect | one strong area hides problems elsewhere | inspect H3, H5, H6, and H9 separately from visual quality |
| Anchoring | the first page sets the severity frame | rate each page/state on its own evidence |
| Familiarity bias | the evaluator knows where things are | ask how a first-time user would recognize the path |
| Confirmation bias | the audit finds what the evaluator expected | search for disconfirming evidence before accepting severity 3-4 |
| Severity inflation | critique sounds sharper than evidence supports | require evidence refs or lower confidence |
| Severity deflation | real friction is softened as "just edge case" | check audience context, stakes, and ability cost |
| Cultural bias | local conventions are treated as universal | ask whether the target audience would read the pattern differently |

## When To Stress-Test A Finding

Use `stress_test_heuristic_finding` when:

- the rating is 3 or 4
- the evidence is mostly inference
- the issue is expensive to fix
- the finding depends on audience context
- the finding is in H11, H12, H13, or H14 and may be culturally or contextually sensitive
- the audit result is unusually harsh or unusually clean

The tool should check alternative explanations, false-positive risk, evidence limits, and one concrete fix.

## Bounded critique pass

Select the one to three findings most likely to change the decision. Use the callable `stress_test_heuristic_finding` through [the bridge](mcp-bridge.md), supplying the actual `checklist_item_id`, rating, neutral rationale, platform and evidence refs. Inspect its alternative explanation, false-positive check, evidence limit and fix suggestion. These are diagnostic prompts, not a second observed audit. Preserve source limits even if the tool returns a confidence label or an empty limitation field; neither establishes evidence coverage.

Recheck the relevant interface anchor or task where feasible. Record `retain / qualify / revise / discard`, the reason, revised severity/confidence if warranted, and the evidence still needed. Check the proposed fix against task success and new risks. If the tool is absent, perform and label an internal critique with these same questions; do not claim a tool call or independent review. Do not automatically lower severity or accept a fix because a tool suggested it.

For independent reviewers or simulated task contexts, use Design Studio's [decision alternatives](../../design-studio/references/decision-alternatives.md). The shared Work Management method governs worker independence and synthesis; repeated or agreeing lenses are not empirical corroboration.

## Debiasing Moves

Use these before report generation:

- Restate the finding neutrally.
- Name the exact evidence ref.
- Name the assumed user context.
- Ask what evidence would lower the rating.
- Ask what evidence would raise the rating.
- Compare the issue against another audience context.
- Separate "I dislike this" from "this blocks, slows, excludes, or misleads users."

## Human-Loop Calibration

Ask the user when:

- the target audience is not obvious
- the task is high stakes
- the interface is for users with limited resources, devices, language access, or institutional familiarity
- optional inclusion or accessibility profiles are active
- the host is about to recommend a major redesign from limited evidence

If the user supplies context that changes severity, note it in the report as calibration context, not as newly observed interface evidence.
