# Oppia Research Question Framing Framework

Load this reference for difficult framing, audits of an existing question set,
or prioritization of an Oppia research backlog. For a simple rewrite, the main
skill is sufficient.

## Question Architecture

Keep the inquiry traceable in both directions:

1. **Signal:** what prompted concern, with evidence strength labeled.
2. **Problem frame:** affected actors, context, observable condition,
   consequence, evidence, uncertainty, and boundary.
3. **Decision:** the choice that could change, its owner, timing, and
   guardrails.
4. **Evidence gap:** what is unknown, disputed, assumed, stale, or outside the
   historical Oppia corpus.
5. **Research question:** the inquiry needed to reduce enough uncertainty for
   the decision.
6. **Research learning objective:** what the team must identify, describe, map,
   compare, assess, distinguish, determine, or explain.
7. **Evidence test:** what observations, accounts, measures, artifacts, logs,
   or comparisons would support and challenge an answer.
8. **Study instrument:** the later task, prompt, measure, or source that would
   produce the evidence.

Every instrument item should support an objective; every objective should map
to a question; every primary question should influence a decision. This skill
stops before writing the full instrument.

## Layer Test

| Layer | Its job | Oppia example |
| --- | --- | --- |
| Signal | Describe the trigger | Several historical notes mention difficulty identifying the next lesson. |
| Problem statement | Bound the condition and consequence | Returning mobile learners may not recognize grouping and sequence cues, delaying lesson selection. |
| Problem question | Open the problem without prescribing a response | What helps or prevents returning learners from choosing an appropriate next lesson? |
| Decision question | State the product choice | Should Oppia change terminology, sequence cues, navigation structure, or another part of the pathway? |
| Research question | Define the inquiry | How do returning mobile learners interpret grouping and sequence cues when choosing a next lesson, and where do their choices diverge from the content model? |
| Learning objective | State the needed knowledge | Identify the cues, interpretations, and mismatch-recovery patterns used during lesson selection. |
| Hypothesis | State a challengeable expectation | Curriculum labels may work for some formally schooled learners but not for all educational contexts. |
| Participant prompt | Elicit evidence neutrally | What would you expect to find if you opened this group? |
| Measure | Operationalize quantitative evidence | Independent selection of a lesson matching the stated goal in the tested flow. |
| How might we | Frame ideation after evidence | How might we make grouping and progression legible without assuming one curriculum vocabulary? |

## Problem Frame

Use this structure:

> **[People or actors]** in **[context]** encounter **[observable condition]**,
> which contributes to **[consequence]**. Existing evidence shows
> **[source-labeled signal]**, but it remains unclear **[gap]**. This frame
> currently excludes **[boundary]**.

Keep symptom, possible cause, and consequence separate. “Learners abandon the
page” is a signal. “The labels are confusing” is one possible explanation.
“Reduced lesson access” is a possible consequence. Do not promote a possible
cause to fact without evidence.

Use the solution-removal test when the request starts with a feature:

1. set the proposed solution aside;
2. name the user outcome it is meant to improve;
3. identify who encounters the current difficulty and where;
4. inspect how they accomplish the goal now;
5. preserve competing explanations and alternative response types;
6. reintroduce the solution later as one option to evaluate.

## Decision Test

Write:

> **[Owner]** must decide **[choice]** by **[date or phase]**, using research to
> reduce uncertainty about **[gap]**, while respecting **[user, equity,
> privacy, safety, policy, or operational guardrails]**.

Then complete at least two branches:

| Plausible answer | Different action or priority |
| --- | --- |
| Answer A | Action A |
| Answer B | Action B |
| Mixed or unresolved | Guardrail, monitoring, narrower release, or defer |

If every branch ships the same selected solution, the work is approval theater
or the decision has already been made. Research can clarify consequences, but
it does not settle value judgments, acceptable risk, legal compliance, or
resource allocation.

## Question Forms And Evidence

Choose the form from the uncertainty, not from a writing formula:

| Need | Useful form | Evidence implication |
| --- | --- | --- |
| process or experience | How do…? | observed sequence, accounts, artifacts, context |
| pattern or variation | What patterns…? / In what ways…? | comparable cases with negative cases |
| barrier or support | What factors…? / Under what conditions…? | breakdowns, supports, alternative explanations |
| interaction evaluation | Where, when, and why does…? | task behavior, interpretations, system states |
| comparison | How does X differ across…? | aligned constructs and comparable conditions |
| meaning | How do people interpret…? | paraphrase, prediction, choices, language/context |
| relationship | What is the relationship between…? | aligned measures without automatic causal claim |
| prevalence | What proportion…? | defined denominator, frame, timeframe, uncertainty |
| change over time | How does… change…? | repeated or longitudinal evidence and version log |

Evidence boundaries matter:

- observation supports behavior in the observed context, not all-user
  prevalence;
- retrospective accounts support remembered experience, not perfect behavioral
  reconstruction;
- preferences support reported preference, not adoption;
- purposive qualitative samples support bounded patterns and explanations, not
  population estimates;
- analytics show instrumented behavior, not motives or excluded non-use;
- experiments support causal claims only when design and analysis justify them;
- historical research transfers only when consent, population, context,
  product state, timing, and method fit remain suitable.

## Focus And Neutrality Repairs

Operationalize loaded abstractions by naming what could be observed or
compared:

- `understand` -> accurate paraphrase, consequence prediction, appropriate
  application, or transfer;
- `trust` -> confidence calibration, verification, reliance, disclosure,
  recovery, or refusal by risk condition;
- `engagement` -> a named behavior and timeframe such as persistence, return,
  contribution, or depth of use;
- `easy` or `intuitive` -> discoverability, independent completion, effort,
  errors, recovery, confidence, or accessibility burden;
- `value` or `usefulness` -> goal progress, replacement of existing work,
  consequence of absence, trade-off, or repeated use.

Split a question when its parts can fail independently, require different
evidence, concern different populations or contexts, or lead to different
actions. Preserve multiple clauses only when they describe one coherent process
or relationship.

Neutrality requires more than changing “do” to “how.” Identify the hidden
premise, preserve at least one alternative explanation, permit support,
rejection, mixed results, and non-use, and define disconfirming evidence.
Established harm does not need to be rhetorically doubted; investigate its form,
conditions, consequences, and remedies.

## Inclusive Scope

Ask which variation can change meaning or access: role, learning context,
language, literacy practice, disability/access need, assistive technology,
device, connectivity, data cost, shared-device use, age, geography, power, and
institutional setting. Include a dimension because it affects the question, not
because demographic detail makes the sentence look rigorous.

Avoid treating nationality, “developing countries,” disability, low literacy,
or limited connectivity as personal deficits. Frame how product, curriculum,
language, infrastructure, policy, and social conditions interact with people.
Name non-users and excluded people when the current surface prevents them from
appearing in product data.

## Question-Set Prioritization

Classify each item:

- **primary:** necessary for the immediate decision;
- **secondary:** useful only if it does not dilute the primary inquiry;
- **deferred:** relevant to another decision, population, phase, or method;
- **remove:** duplicate, already answered, unanswerable, rhetorical,
  misclassified, or unable to change action.

Prioritize by consequence of unresolved uncertainty, current uncertainty,
decision urgency, reuse value, feasibility and evidence access, and ethical or
inclusion risk. Stakeholder seniority and vote count are not evidence of
research value.

## Review Of AI-Generated Questions

When AI assists framing:

1. compare every element with the source request and Oppia evidence;
2. flag invented populations, metrics, deadlines, decisions, or findings;
3. classify each line by question layer;
4. check whether a yes/no question was merely rewritten with “how”;
5. count constructs, populations, contexts, and intended claim types;
6. test decision branches, solution bias, and alternative explanations;
7. require supporting and challenging evidence;
8. inspect cultural, accessibility, and power assumptions;
9. retain accountable human judgment and a revision record.

Fluency, length, or a numeric rubric score does not make a question valid.

## Approval Gate

Before handoff, confirm:

- the signal's evidence status and limits are visible;
- the problem frame remains provisional and revisable;
- a consequential decision or legitimate strategic inquiry is explicit;
- the primary question is neutral, focused, answerable, feasible, ethical,
  inclusive, and distinct;
- question, objective, evidence, and claim boundary align;
- contradictions, alternate explanations, and disconfirming evidence remain
  possible;
- secondary curiosity is deferred rather than packed into the same study;
- the next method lane is singular, justified, and limited.
