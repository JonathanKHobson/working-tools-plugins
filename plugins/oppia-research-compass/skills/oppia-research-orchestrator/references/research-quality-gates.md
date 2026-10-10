# Oppia Research Quality Gates

These gates apply after the Oppia corpus has been searched and before a new
study, synthesis, persona change, CUJ change, or recommendation is treated as
decision-ready. They are adapted from the reviewed external UX research skill
archive recorded as `external.ux-research-skill.v1.0.0` in the source register.

## 1. Decision And Method Fit

Start with a decision, not a preferred method:

> Decide **[choice or action]** for **[people and context]** by **[date or
> event]**, based on evidence about **[uncertainty]**, while protecting
> **[critical guardrail]**.

Choose the smallest method that can produce the needed evidence. State what it
can and cannot establish:

| Needed evidence | Suitable starting lane | Cannot establish alone |
| --- | --- | --- |
| prior Oppia finding or known gap | Oppia MCP retrieval | current behavior after a material change |
| language, motivation, context, mental model | interviews | directly observed task performance or prevalence |
| behavior on a task or flow | usability testing | population prevalence or long-term adoption |
| interface risk without participants | heuristic evaluation | observed user impact |
| comparable product pattern | competitive analysis | Oppia user need or effectiveness |
| public community discourse | provisional netnography | representativeness or prevalence |
| behavioral grouping | persona research | decorative biography or universal segments |
| end-to-end goal path | CUJ research | production verification without tests or metrics |

## 2. Evidence Chain

Keep each stage traceable and distinct:

1. source;
2. observation, report, or measurement;
3. code or category when analysis requires it;
4. pattern or finding;
5. interpretation or insight;
6. implication or opportunity;
7. recommendation with owner, risk, and validation need;
8. accountable product or organizational decision.

For consequential claims, preserve source IDs, sample or denominator,
population and context, product version or date, counterevidence, alternative
explanations, confidence rationale, and the decision implication. A generated
summary is not a source.

## 3. Sample Rationale Without Magic Numbers

Do not default to a universal participant count. Name the intended claim and
use method-appropriate logic:

- For qualitative work, justify coverage using question focus, participant and
  context variation, depth of evidence, analytic approach, decision risk, and
  an iterative stopping rule.
- Continue only while new sessions could change the decision-level explanation,
  reveal critical negative cases, or fill required context coverage.
- For estimates or experiments, require a statistical rationale based on the
  target quantity or effect, uncertainty, design, nonresponse or attrition, and
  subgroup needs. Do not substitute a qualitative rule of thumb.
- State what the achieved sample supports and what it does not.

## 4. Pilot And Change Control

Pilot the complete participant or evaluator experience, not only the question
list. Verify invitation, consent, tasks or stimuli, accommodations, timing,
technology and fallback paths, evidence capture, analysis readiness, closing,
and storage.

Record material changes with version, reason, affected sessions, and whether
pre-change evidence remains comparable. Re-pilot critical sections after a
research-question, task, stimulus, instrumentation, or procedural change.

## 5. Contradictory And Negative Evidence

Write contradictions explicitly. Check whether sources share the same
question, construct, denominator, population, context, product version, and
timeframe. Examine role, goal, experience, device, language, access need,
workflow stage, observed-versus-reported evidence, protocol deviations, and
instrumentation before averaging or choosing a preferred source.

The decision response may be to segment, narrow a rollout, add a guardrail,
investigate, monitor, or accept a visible trade-off. Keep unresolved conflicts
beside the recommendation with an owner or revisit trigger.

## 6. Inclusion, Culture, Ethics, And Privacy

- Treat disability, language, culture, infrastructure, age, socioeconomic
  context, and power as validity conditions when they affect the Oppia decision.
- Plan relevant assistive technologies, accommodations, device and bandwidth
  conditions, translation or interpretation, and accessible alternatives.
- Do not treat geography or demographic identity as a proxy for behavior.
- Confirm consent, secondary-use permission, access, minimization, retention,
  withdrawal, and participant protection for the actual study and local policy.
- Escalate consequential legal, safeguarding, privacy, accessibility, or
  statistical questions to the accountable Oppia owner; this plugin does not
  certify compliance.

## 7. AI-Assisted Research

Before using AI with research material:

1. confirm the tool is permitted to process that data;
2. minimize and de-identify inputs while preserving needed context;
3. require stable source IDs for consequential claims;
4. compare outputs with a human-reviewed subset and test omissions,
   contradictions, minority experiences, and fabricated detail;
5. keep the original evidence accessible;
6. record the tool or model, procedure, inputs, reviewer, changes, and limits;
7. require accountable human review before participant contact, findings,
   recommendations, or decisions;
8. disclose material AI assistance when it affects interpretation, policy, or
   stakeholder trust.

## Release Gate

A research artifact is ready only when the decision, corpus search, method fit,
evidence chain, inference boundary, contradictory evidence, inclusion and
privacy conditions, pilot/change status when applicable, limitations, owner,
and stop condition are visible. Missing items remain explicit gaps; they are not
filled with plausible language.
