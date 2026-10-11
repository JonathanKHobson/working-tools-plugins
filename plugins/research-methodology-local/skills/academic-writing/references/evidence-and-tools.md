# Academic argument and tool checks

Use for a requested scientific argument audit or manuscript revision. Ordinary proofreading does not need this pass. Academic Writing Toolkit remains the provider of its existing tools; this reference adds judgment and handoffs rather than duplicating those tools or modifying vendor files.

## Evidence before polish

For each consequential conclusion, identify the concrete problem, what the proposed method changes, the expected observable consequence, and the supplied evidence. Keep a short claim-to-evidence table only when several claims need tracking. Separate these evidence types:

Final argument check: **problem → mechanism → observable consequence → evidence → scope**. If a link is only proposed, label it as a hypothesis; if the evidence supports only one dataset, population, or protocol, keep the conclusion there.

| Evidence | What it can establish |
| --- | --- |
| Derivation | A result within the stated assumptions |
| Implementation | What the system computes or does |
| Controlled ablation | The effect of the isolated change under that protocol |
| Comparison of complete methods | A difference between those methods in the tested conditions |
| Diagnostic measurement | Whether an expected intermediate behavior occurred |

A comparison of bundled methods does not isolate one component's causal contribution. Correlated changes do not establish a mechanism. Keep independent explanations separate rather than inventing one causal story. Label an untested mechanism as a hypothesis or design intent; even “reduces risk” needs evidence when stated as an observed effect.

Preserve supplied numbers, equations, symbols, definitions, metrics, datasets, protocols and scope. Return proposed conceptual corrections separately from prose edits. Check that abstract, introduction, methods, results and conclusion make compatible claims; a conclusion must not expand the population or conditions actually studied. For reviewer responses, distinguish an edit made from an experiment proposed or completed.

Check source existence, identity, claimed location and support for the exact statement; use `evidence-review` for the research evidence audit and the available Writing Quality Studio deep audit when its citation tools help. Missing evidence stays unresolved or the claim is narrowed; a fluent explanation cannot fill the gap.

If the user requests a methodological critique of supplied manuscript content and Critical Compass is available, use its guided `audit_text` or `claim_stress_test` as a diagnostic aid. Follow [its integration boundary](../../../docs/critical-compass-integration.md) for consent and provenance. It does not replace source verification or Academic Writing Toolkit's drafting and citation tools.

## Diagnose the technical problem and mechanism

Before accepting a claimed solution, state a behavior that can be observed under a defined condition, along with the current or prior design's limitation. A paper saying it needs another module or greater robustness has described a proposed design or aspiration; ask what actually goes wrong, for whom or in which operating regime. Use the supplied measurements, requirements or documented failure trace. Do not invent the missing baseline.

Locate the intervention in the actual model, algorithm or system description. Identify the changed element by its source identifier when available: a quantity or parameter, a relationship between quantities, a permitted set of decisions, an update/scheduling rule, a computation interval, or the movement of information between components. Explain its before/after behavior and the intermediate consequence that should follow under the stated assumptions. If the manuscript does not specify that change, flag the missing mechanism instead of substituting a broad benefit.

Check whether the evidence measures the intermediate behavior, the final task outcome, or both. A diagnostic showing a changed internal quantity can support the mechanism explanation without proving task-level superiority. Conversely, a higher final score after several simultaneous changes does not isolate the proposed mechanism. Require an appropriate control, a direct diagnostic or narrower wording for that attribution. Preserve parallel explanations where more than one cause remains plausible.

For a consequential claim, a useful record is: observed problem and setting; limitation of prior design; identified intervention; expected intermediate effect; actual evidence/assumptions; supported conclusion and remaining test. Equations, implementation passages, figures and experiments each need a role in that record. Missing links remain unresolved or the claim is narrowed.

For example, a manuscript replaces a fixed retry delay with an adaptive rule. Identify the delay variable and update rule from the supplied method, what input governs it, and which workload was tested. A lower average completion time for a version that also changes concurrency cannot establish the adaptive-delay effect by itself. A proposed isolated comparison is a next test, not a completed result.

## Use only the relevant existing tool

When Academic Writing Toolkit is available and the task calls for it:

- `create_reading_note_template`: prepare structured notes; replace placeholders with actual source information. It creates no evidence itself.
- `audit_citations`: compare pasted prose with reading-note `**Source**` lines in the selected style. Use the template's syntax if the parser rejects a line; distinguish formatting errors from missing sources.
- `verify_bibtex_references`: check pasted BibTeX offline. Field validity is not proof that a publication exists or supports a claim.
- `review_paragraph_logic`: obtain deterministic review cues, then assess the argument directly. A clean result is not a scientific validity judgment.
- `check_british_english`: use only for the requested spelling convention. Preserve quoted text, proper names and the publication's own requirements.

Provide only the relevant authorized material to a connector. If a tool is unavailable or errors, state which check did not run and perform a clearly labeled manual check when feasible. Do not install a substitute service or silently equate a manual review with tool verification.

Follow the actual target journal's current author requirements. No blanket ban on colons, italics or punctuation is implied by an Elsevier or COMPAG label. Finish with exact locations, evidence, proposed changes and unresolved questions; return the revised text first when that is the requested deliverable.

Basis: Research Writing Guardrails marketplace entrypoints inspected 2026-09-28; Academic Writing Toolkit's five live tool schemas and synthetic probes. This is original local guidance; external instruction files and code were not imported.
