# Feedback Surveys

## Start with the trigger and decision

“Feedback survey” can mean a one-question intercept, post-task measure, post-support survey, relationship tracker, beta evaluation, employee pulse, or open suggestion form. Define:

- the exact experience or relationship being evaluated;
- when the invitation appears;
- who is eligible;
- what decision the result informs;
- whether the need is monitoring, diagnosis, prioritization, or discovery.

## Lean product-experience pattern

For a recent, specific experience:

1. **Context/behavior:** What was the respondent trying to do? Did they complete it?
2. **Primary outcome:** One construct such as ease, satisfaction, confidence, or perceived value.
3. **Diagnostic:** Main obstacle/reason, preferably closed categories based on prior research.
4. **Open follow-up:** One optional focused prompt.
5. **Follow-up consent:** Separate contact field or link when interviews may be useful.

A two-question survey can be excellent: one outcome and one diagnostic open end. Do not add demographics, loyalty, brand, and feature voting merely because the respondent is present.

## Transactional vs relationship

| Design | Trigger | Measures | Strength | Risk |
|---|---|---|---|---|
| Transactional | immediately after a defined event | event outcome, effort, resolution | better recall and diagnosis | event/mode selection bias |
| Relationship | periodic sample | overall experience, trust, loyalty | broader trend | vague recall and low actionability |

Do not compare them as if they measure the same population and timeframe.

## Common metrics

- **CSAT:** satisfaction with a named object and timeframe. Record scale and scoring convention.
- **Ease/effort:** perceived difficulty or effort for a specific task. Keep direction explicit.
- **NPS:** 0–10 likelihood-to-recommend item used in some programs. Preserve wording/scoring for trend continuity; do not treat it as a full diagnostic or universal growth predictor.
- **Task success:** self-reported or observed completion; define partial success and verify with behavior when available.
- **Confidence/trust:** name the object and context; these are distinct constructs.
- **Open-text themes:** diagnostic qualitative data, not a denominator-free substitute for prevalence.

## Feature feedback

Avoid “Would you use feature X?” as the sole input. Better evidence includes current workaround, frequency of the problem, consequence, context, willingness to switch/pay under realistic conditions, concept comprehension, and observed prototype behavior.

Roadmap voting overweights people who respond and features that are easy to describe. Pair stated preference with problem severity, strategic fit, technical cost, and behavioral evidence.

## Trigger governance

- Define frequency caps and cooldowns.
- Avoid interrupting urgent, high-stakes, or failed flows before recovery help.
- Suppress known bots, internal testers, duplicate events, and repeated completions.
- Track trigger exposure so nonresponse can be assessed.
- Ensure dismissal is easy and does not block the task.
- Offer accessible channels and avoid relying solely on an in-product surface that excludes former or unsuccessful users.

## Close the loop

A feedback program needs owners, review cadence, issue-routing rules, respondent follow-up consent, and communication about changes. Repeatedly collecting feedback without visible action can reduce trust and response quality.

## Reuse across experiences and entry points

Reuse one versioned instrument across channels when the decision and constructs are the same. Separate experience context (what was evaluated) from collection source (how the respondent arrived). Supply reliably known context through trusted metadata rather than redundant questions. For generic links, establish missing context explicitly rather than guessing. Keep wording/codes stable for intended comparisons and retain historical versions when they change.

Choose length and questions from the decision, audience and burden target. Two ratings plus an optional diagnostic comment is one useful short pattern, not a default for every survey. The [learning-experience example](../examples/learning-experience-feedback.json) illustrates reuse across course and workshop delivery; it is an unfielded example, not a required template. Perceived confidence is not demonstrated learning, and completion analytics are not satisfaction measures.

Treat an existing survey as evidence about its observed structure, not proof of validity in a new context. Do not invent unseen scale options or carry audience-specific content into unrelated instruments. Preserve sampling and nonresponse limits when comparing channels or experiences; one shared form does not make populations interchangeable.

When implementation is requested, use [survey implementation](survey-implementation.md). Keep a form or collection-flow request bounded; discussion of administration, dashboards or analytics does not automatically require a survey-management product.
