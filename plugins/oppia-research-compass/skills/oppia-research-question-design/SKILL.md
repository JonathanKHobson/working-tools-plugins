---
name: oppia-research-question-design
description: Use when an Oppia team member needs to turn a vague request, reported problem, assumption, metric change, proposed solution, or question backlog into focused, neutral, decision-linked UX research questions. Do not use when the historical corpus already resolves the decision or when approved questions only need a study instrument.
---

# Oppia Research Question Framing

## Overview

Frame the uncertainty before choosing a research method. This skill owns the
focused step between a raw Oppia request and an approved question set. It does
not own full study design, participant recruitment, discussion guides, or
findings synthesis.

Search Oppia's historical evidence first. A strong outcome may be a framed
question, a smaller evidence gap, a non-research route, or a decision to defer.

Source anchors: `drive.oppia.research-question-log.v1`,
`drive.oppia.research-synthesis.v1`,
`external.ux-research-skill.v1.0.0`, and
`external.research-question-framing-skill.v1.0.0`.

For a complex request, question audit, or backlog, load
[references/question-framing-framework.md](references/question-framing-framework.md).
Use [assets/oppia-research-question-framing-card.md](assets/oppia-research-question-framing-card.md)
when a reusable handoff artifact is needed.

## Workflow

1. **Capture the signal without upgrading it into fact.** Record whether the
   trigger is direct evidence, a stakeholder report, metric, complaint,
   assumption, opportunity, or proposed solution.
2. **Search the Oppia corpus.** Use `oppia_research` for broad discovery and
   `search_oppia_research` for a focused query. Retrieve evidence that will be
   quoted and preserve its `evidence_id`, population, context, date, product
   state, and limitations.
3. **Write a provisional problem frame.** Name the affected people or actors,
   context, observable condition, consequence, known evidence, unresolved gap,
   and explicit boundary. Keep multiple explanations open.
4. **Recover the decision.** Name the accountable owner, actual choice,
   decision date or phase, uncertainty, and user, equity, privacy, safety, or
   operational guardrails. Research supplies evidence; it does not decide
   values, acceptable risk, policy, or resource allocation.
5. **Run the decision-branch test.** Write at least two plausible answers and
   the meaningfully different actions each would support. If every answer leads
   to the same action, reframe, deprioritize, or remove the question.
6. **Separate the layers.** Distinguish signal, problem statement, problem
   question, decision question, research question, research learning objective,
   hypothesis, participant prompt, measure, and post-evidence ideation prompt.
7. **Write one primary research question.** Add no more than three supporting
   questions when each is necessary for the same decision. Move adjacent
   curiosity to secondary, deferred, or remove.
8. **Operationalize vague constructs.** Replace words such as understand,
   trust, engagement, value, easy, intuitive, or successful with the behavior,
   interpretation, relationship, variation, or measure that would count as
   evidence in this Oppia context.
9. **Remove bias and overload.** Expose hidden premises, remove the favored
   solution from the question, keep confirming and disconfirming outcomes open,
   and split clauses that require different evidence or decisions.
10. **Map question to evidence.** For every primary question, name supporting
    and challenging evidence, the source or method capable of producing it,
    the strongest justified claim, prohibited claims, and material validity
    threats.
11. **Check inclusion and feasibility.** Include language, disability/access
    needs, device, connectivity, educational context, age, socioeconomic
    conditions, and power only when they affect the phenomenon or decision.
    State missing voices and disproportionate burden rather than treating a
    country or demographic label as a behavioral explanation.
12. **Hand off one bounded job.** If a real gap remains, recommend the smallest
    method lane that can answer it and state what that method cannot establish.

## Question Quality Gate

A primary question is ready only when it passes all applicable checks:

- **Decision relevance:** plausible answers could change a real Oppia choice.
- **Neutrality:** support, rejection, mixed, and unexpected outcomes remain
  possible.
- **Focus:** one coherent phenomenon, process, or relationship is central.
- **Population and context:** necessary boundaries are explicit without false
  demographic precision.
- **Answerability:** authorized evidence and a feasible method can address it.
- **Observable evidence:** the team can name what would support and challenge
  an answer.
- **Claim discipline:** wording does not invite unsupported causality,
  prevalence, universality, or prediction.
- **Ethics and inclusion:** the question is worth the burden and avoids deficit
  framing, coercion, exclusion, or unjustified sensitive-data collection.
- **Distinct value:** it is not already answered, duplicated, a participant
  prompt, a deliverable, a method, or an ideation question.

Critical failure overrides polished wording. Do not approve a question whose
only acceptable outcome validates a selected solution, whose evidence path is
unethical, or whose intended claim cannot be supported.

## Output Contract

For a simple rewrite, return:

- original wording;
- revised wording;
- why the revision is stronger;
- one remaining assumption, limitation, or evidence gap.

For substantive framing, produce an Oppia RQ framing card containing:

- triggering signal, source, evidence status, and what it does not establish;
- provisional problem frame and scope boundary;
- decision, owner, date or phase, constraints, and two decision branches;
- existing Oppia evidence IDs, non-findings, contradictions, and freshness
  limits;
- one primary research question and necessary supporting questions;
- research learning objectives mapped to question IDs;
- evidence alignment: support, challenge, source/method, strongest claim,
  prohibited claim, and validity threat;
- assumptions, alternative explanations, inclusion/ethics risks, and missing
  voices;
- secondary, deferred, and removed questions with reasons;
- recommended next lane, method limit, evidence threshold, and stop condition.

## Stop Conditions

- Stop at an evidence brief when the Oppia corpus already resolves the decision.
- Stop at a clarification when the uncertainty is product logic, engineering,
  policy, strategy, or an unresolved value choice rather than a user-research
  question.
- Stop after the smallest decision-sufficient question set; do not produce a
  full research plan, participant script, survey, or workshop unless separately
  requested.
- Do not invent a problem, population, decision, deadline, or evidence gap.
  Mark missing elements and proceed with explicit assumptions only when they do
  not materially change the framing.
- Treat “How might we” as post-evidence ideation, not as a research question.
- Do not open a new study merely because historical evidence has limitations.

## Verification

- The signal remains labeled as direct, reported, inferred, assumed, or
  unknown.
- Existing Oppia evidence was searched, cited by stable ID, or explicitly found
  absent.
- The problem frame describes an observable condition and consequence rather
  than the absence of a preferred feature.
- At least two plausible answers support meaningfully different actions.
- Research questions, learning objectives, hypotheses, participant prompts,
  measures, and ideation prompts are not mislabeled as one another.
- Each primary question has supporting and challenging evidence plus a clear
  claim boundary.
- Leading, solution-biased, double-barreled, deficit-based, and vague wording is
  repaired.
- Relevant language, accessibility, connectivity, educational context, and
  power conditions are represented or recorded as gaps.
- The handoff selects one next lane and states its limit.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UX Researcher. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
