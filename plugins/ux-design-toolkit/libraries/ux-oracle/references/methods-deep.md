# UX Oracle Methods Deep Guide

## Contents

- Method selection logic
- Recommended method stacks
- Phase-by-phase guidance
- Resource-based guidance
- Method notes
- Common mistakes

## Method selection logic

Start with the question type, then check product phase, constraints, and evidence gaps.

### Question type -> method family

- `Why is this happening?`
  - Use qualitative methods such as interviews, contextual inquiry, diary studies, or session review.
- `How many, how often, or which segment?`
  - Use quantitative methods such as surveys, analytics, benchmark studies, or first-click tests with measurable outcomes.
- `Does this design work?`
  - Use evaluative methods such as usability testing, heuristic evaluation, cognitive walkthroughs, accessibility audits, or A/B testing.
- `What should we build or prioritize?`
  - Use generative methods such as interviews, co-design, JTBD interviews, card sorting, tree testing, or concept testing.

### Phase -> default method posture

- `Discover`
  - Prioritize generative methods.
  - Seek behaviors, unmet needs, context, and workarounds.
- `Define`
  - Prioritize synthesis and framing.
  - Translate raw data into insights, tensions, and opportunity areas.
- `Develop`
  - Combine concept validation with IA and flow testing.
  - Use card sorting, tree testing, concept tests, and lightweight usability studies.
- `Deliver`
  - Prioritize evaluative methods.
  - Measure whether users can complete tasks efficiently, confidently, and accessibly.

### Constraints -> rigor adjustment

- `0-1 week, no budget`
  - Use heuristic evaluation, analytics review, cognitive walkthrough, or guerrilla testing.
  - Pair one fast method with one lightweight validation method.
- `1-3 weeks, limited budget`
  - Use 5-8 interviews or usability tests plus a short survey or analytics pass.
- `3+ weeks, moderate support`
  - Use benchmark studies, diary studies, mixed-method research, or deeper fieldwork.

## Recommended method stacks

Prefer a primary method plus a validation method.

| Need | Primary method | Validation method |
|---|---|---|
| Choose between concepts | Concept test | Follow-up interview |
| Diagnose a broken flow | Moderated usability test | Heuristic evaluation |
| Understand unmet needs | Semi-structured interviews | Survey or analytics review |
| Fix navigation or labeling | Card sort or tree test | First-click test |
| Measure baseline usability | Benchmark study or SUS | Moderated task study |
| Understand behavior over time | Diary study | Follow-up interview |
| Prioritize opportunity areas | Affinity mapping + HMW | Stakeholder alignment workshop |

## Phase-by-phase guidance

### Discover

Use when the team does not yet understand user context or unmet needs.

- Best methods:
  - interviews
  - contextual inquiry
  - ethnographic observation
  - diary studies
  - JTBD interviews
- Watch for:
  - confirmation bias from product hypotheses
  - over-reliance on vocal power users
  - users describing ideals rather than actual behavior

### Define

Use when the team has raw data and needs insight, framing, or prioritization.

- Best methods:
  - affinity mapping
  - thematic analysis
  - JTBD framing
  - opportunity mapping
  - journey mapping
- Watch for:
  - naming clusters descriptively instead of insightfully
  - skipping tensions between user groups
  - turning hypotheses into facts

### Develop

Use when the team has concepts, IA, or flows to shape before building deeply.

- Best methods:
  - co-design workshops
  - card sorting
  - tree testing
  - concept testing
  - low- to mid-fidelity usability testing
- Watch for:
  - testing visuals when the real question is IA
  - anchoring too hard on the first concept
  - asking users to design instead of react, decide, or prioritize

### Deliver

Use when the product is close to launch or in-market and needs validation.

- Best methods:
  - moderated usability testing
  - unmoderated task testing
  - heuristic evaluation
  - accessibility audit
  - A/B or multivariate testing
- Watch for:
  - confusing preference with performance
  - using A/B tests before the design is basically usable
  - measuring completion without measuring confidence or error recovery

## Resource-based guidance

### Small team, minimal access to users

- Start with heuristic evaluation or cognitive walkthrough.
- Add analytics or support-ticket review if available.
- Use guerrilla testing only for coarse signals, not strategic certainty.

### Good user access, but little time

- Run 5 moderated sessions against one core task set.
- Add a short post-test survey or SUS if benchmarking matters.

### Strong research runway

- Combine behavioral qualitative work with a lightweight quant layer.
- Use diary studies or contextual inquiry when environment and time matter.

## Method notes

### Heuristic evaluation

- Best when speed matters and expert critique is acceptable.
- Weakness: it finds probable issues, not user truth.
- Pair with testing if the decision is high stakes.

### Usability testing

- Best for task success, friction, and mental model mismatches.
- Moderated for depth, unmoderated for scale.
- Ask users to attempt realistic tasks, not feature tours.

### Interviews

- Best for motivations, context, and decision-making.
- Ask about recent real behavior first.
- Probe with "what happened next?" more often than "why?"

### Surveys

- Best for prevalence, segmentation, and attitude measurement.
- Use neutral wording and keep scales consistent.
- Do not use surveys to discover nuanced root causes on their own.

### Card sorting

- Best for category structure and labels.
- Open sort for discovery, closed sort for validation, hybrid when some structure exists.

### Tree testing

- Best for findability and IA verification without visual noise.
- Use when navigation or labeling is the core problem.

### Diary studies

- Best for longitudinal behavior, habits, and event-based friction.
- Require clear prompts and strong participant follow-through.

### Accessibility audit

- Best for identifying barriers against WCAG and inclusive interaction principles.
- Combine automated checks with manual keyboard, screen reader, and zoom review.

## Common mistakes

- Choosing one method because it is familiar instead of because it answers the question.
- Asking users what they want when the real need is to observe what they do.
- Treating stakeholder confidence as evidence.
- Using a survey before defining the decision it needs to support.
- Running usability tests without task realism or success criteria.
- Skipping synthesis and jumping from notes straight to solutions.

## Output pattern for method advice

Use this structure when recommending an approach:

```markdown
Mode: Method Advisor

## Recommendation
Primary method: ...
Validation method: ...

## Why this fits
- Question type:
- Phase:
- Constraints:

## Tradeoffs
- ...

## What to collect
- ...

## Confidence
- ...
```
