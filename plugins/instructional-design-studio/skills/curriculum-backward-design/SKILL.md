---
name: curriculum-backward-design
description: Design a course, curriculum, syllabus, or learning pathway by aligning outcomes, authentic evidence, prerequisites, practice, and assessments.
---

# Curriculum & Backward Design

Start with the performance learners should demonstrate in the destination context. Work backward to acceptable evidence, then the learning sequence. Use an existing standard or syllabus when supplied; do not replace it with a preferred framework.

## Build the alignment

Apply [learning beyond the activity](../instructional-design/references/addie-decisions.md#preserve-learning-beyond-the-activity) when defining outcomes and module sequences: name the underlying understanding or capability, its value and evidence beyond completing the course scenario.
Give important outcomes stable IDs. Each outcome should specify an action, conditions, and a defensible success criterion. Use “explain” or “justify” when conceptual understanding is the goal; observable does not mean every outcome needs a speed target or numerical cutoff.

For each outcome, link the need, prerequisites, practice, feedback, final evidence, and later application support. Put prerequisites before dependent work; revisit core ideas across later contexts. Distinguish a course's required core from enrichment. Allocate realistic time for practice, feedback, transitions, and learner setup. A fixed duration is a constraint to test; if it cannot support the outcome, propose a narrower objective or additional practice instead of compressing everything.

Design an authentic culminating task early. A creation outcome cannot be demonstrated solely by recalling definitions. Do not force every lesson through every Bloom level, or present ADDIE as evidence that the course works. Use frameworks as design aids.

## Output
Provide a course brief, module sequence, alignment matrix, culminating-task brief, learner workload, and pilot/revision plan. For academic syllabi include grading weights and support information only when known; flag missing institutional policies rather than inventing them.

For complex maps, use [alignment format](references/alignment-format.md), the [example](assets/alignment-example.json), and `python3 scripts/check_alignment.py <alignment.json>` from this skill directory. It checks coverage and IDs, not cognitive rigor. Manually inspect whether the actual task elicits the claimed skill.

Use [learning science](../instructional-design/references/learning-science.md) for evidence and [design patterns](../learning-needs-analysis/references/design-patterns.md) for scope decisions.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Instructional Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
