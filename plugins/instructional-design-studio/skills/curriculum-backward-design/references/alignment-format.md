# Alignment JSON

Use this optional format for a complex map. The [example](../assets/alignment-example.json) is an illustrative two-outcome lesson, not learner evidence.

Required arrays: `outcomes`, `practice`, `assessments`, `rubric`. Every row has a unique nonempty `id` within its array and `description`. Practice and assessment rows have nonempty `outcome_ids`. Rubric rows have `outcome_id`, `assessment_id`, and positive finite `points`. Top-level `max_points` equals the sum of criterion maxima.

Each outcome needs practice, assessment, and rubric coverage. Each assessment needs a rubric criterion. A rubric criterion's outcome must be one that its assessment covers. Duplicate references and dangling IDs are rejected. Optional extra fields can hold timing, source IDs, thresholds, or access notes.

Run from this skill folder:

```bash
python3 scripts/check_alignment.py assets/alignment-example.json
```

The script reads only the named JSON and writes a result to stdout. It does not validate pedagogical rigor, fairness, source quality, or whether a pass threshold is defensible. Inspect those manually.

