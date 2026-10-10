# UXHC Severity Calibration Guide

Severity is not only about how bad an interface issue looks. It is about how much friction the issue creates for the user, task, device, context, and stakes in front of you.

Use this guide before accepting severity ratings for H7 Flexibility and Efficiency of Use, H13 Customer Journey and Satisfaction, and any high-impact H11/H12 finding.

## Establish Audience Context

Infer the audience from the supplied product and task when that is sufficient. Ask one bounded question only when the missing audience context could materially change a high-impact severity judgment:

```text
Who is the primary audience for this interface, and are there constraints the evidence may not show, such as low bandwidth, shared devices, low literacy, high-stakes tasks, limited time, assistive technology, or mobile-only access?
```

Use the host's available question surface when an answer is necessary. Otherwise proceed with a stated general-audience assumption, mark the affected score's confidence lower, and identify what audience evidence would change it. Do not delay an otherwise useful bounded report solely because this context was not supplied.

## Fogg Ability Axis

UXHC can use the ability-cost idea from the Fogg Behavior Model: behavior depends in part on motivation, ability, and a prompt. For heuristic severity, the most useful axis is **ability**. An external pattern lookup is optional.

When ability cost rises, the same interface friction can become more severe:

- low bandwidth increases loading, retry, and media risk
- low literacy increases copy, form, label, and instruction risk
- low digital familiarity increases recognition, recovery, and navigation risk
- mobile-only use increases target, viewport, interruption, and context-switching risk
- high-stakes tasks increase error prevention and recovery severity
- limited time, stress, or noisy environments increase cognitive-load severity

Do not use this as an automatic score multiplier. Use it as a calibration check: would this issue block, exclude, or meaningfully burden this audience more than a generic user?

## Calibration Table

| Audience context | Raise severity when | Usually do not raise when |
| --- | --- | --- |
| General audience | the issue affects task completion, clarity, recovery, or confidence for most users | the issue is only cosmetic or preference-based |
| Low bandwidth | the interface depends on heavy media, delayed hydration, client-side loading, or retry-prone flows | a static text or layout issue remains readable and actionable |
| Low literacy or second-language users | labels, instructions, errors, or choices require jargon, abstract language, or hidden context | the issue is mostly visual polish and does not affect comprehension |
| High-stakes task | errors could affect money, benefits, health, school, legal status, safety, or trust | the issue does not affect decision quality, completion, or recovery |
| First-generation or underserved users | the design assumes institutional knowledge, high confidence, stable access, or familiarity with official processes | the flow provides clear reassurance, alternatives, and recovery |
| Mobile-constrained users | the problem worsens with small screens, touch targets, interruptions, device sharing, slow network, or limited typing | the issue only appears in desktop-specific affordances |

## Same Issue, Different Audience

### Example 1: Vague Button Label

Generic ecommerce browse page:

- Issue: primary CTA says "Continue" without previewing the next step.
- Likely severity: 2, minor.
- Rationale: hesitation is likely, but recovery is low-risk.

Benefits application on a mobile device:

- Same issue: primary CTA says "Continue" without previewing whether it submits, saves, or advances.
- Likely severity: 3 or 4.
- Rationale: stakes are higher, recovery may be uncertain, and fear of submitting incorrect information can block progress.

### Example 2: Loading State Missing

Simple marketing page:

- Issue: button click has a delayed response and no loading state.
- Likely severity: 1 or 2.
- Rationale: the user may click twice or feel friction, but the task is low-stakes.

Low-bandwidth learning flow:

- Same issue: no loading or progress state after launching an activity.
- Likely severity: 3.
- Rationale: users may think the page failed, refresh, lose state, or abandon the task.

### Example 3: Dense Instructions

Internal tool for trained staff:

- Issue: instructions are long but accurate.
- Likely severity: 1 or 2.
- Rationale: trained users may tolerate the density if task support is available.

Public-facing first-time form:

- Same issue: long instructions before a required action.
- Likely severity: 3.
- Rationale: users may not know which parts matter, increasing error risk and abandonment.

## HIL Rescoring Rules

Raise a score when the user provides context that shows:

- the task is higher-stakes than the evidence suggested
- the audience has lower ability for the task conditions
- a missing state is common in real use, not an edge case
- the issue compounds across a journey or repeated use
- recovery is costly, embarrassing, confusing, or unavailable

Accept the existing score when:

- the audience context does not change task risk
- the issue remains cosmetic or easily recoverable
- the evidence is too weak and should instead lower confidence
- the user preference is aesthetic, not usability-impacting

Lower confidence instead of changing severity when:

- the state was not observed
- audience context is plausible but unconfirmed
- code suggests a risk that rendered evidence does not show
- the issue depends on analytics or participant behavior not supplied

## When To Use `stress_test_heuristic_finding`

Use `stress_test_heuristic_finding` when:

- a finding is rated 3 or 4
- audience context changed the rating
- the finding may reflect evaluator preference
- evidence is thin but the recommendation would be costly
- H11/H12/H13 findings are being used to justify a major product decision

The goal is not to weaken the critique. The goal is to make the severity defensible.
