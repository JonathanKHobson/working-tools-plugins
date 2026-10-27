# Change review and repository audit

Use from `review-and-release` for an explicitly requested code review or codebase audit. This is a one-shot report. It does not change the implementation mode or edit code unless fixes are authorized. Full licensed source lineage is in [adoption](../docs/efficient-implementation-adoption.md).

Priority: correct, safe, works at the expected load, meaningfully tested, sufficiently fast, then simple to maintain.

## Establish the target and trace the behavior

For a change review, use the named files, staged/uncommitted diff, branch or PR. Without a named target, inspect uncommitted changes, or the last commit if the tree is clean, and state the target. Read the diff plus affected callers, callees, tests and relevant README. A signature, return shape or behavior change requires checking every caller, including configuration, fixtures and dynamic references.

For a whole-repository audit, use the named folder/package or repository. Read entry points, dependencies, build/deploy configuration, tests and README. Trace important flows from input through storage to output: authentication, money, user input, writes, jobs and shared state. In a large repository, go deepest where failure is consequential and identify coverage limits.

Find expected load in project evidence. A one-user script and a service running in many processes have different needs. State any assumption instead of inventing production scale. Check the implementation contract and the incumbent behavior, including relevant human-facing requirements.

## Inspect

1. **Correctness:** wrong results, crashes, empty/zero/last-item cases, rounding, dates/time zones, inconsistent rules, broken consumers, or a local patch leaving the shared cause intact.
2. **Security and data integrity:** injection, weak randomness, secrets, unvalidated external input, unsafe paths, swallowed errors, write ordering, transactions, authorization and privacy.
3. **Load:** check-then-write races, duplicated work across processes, unbounded collections/memory, query-per-item behavior, quadratic work on large inputs and process-local state that must be shared.
4. **Tests:** risky behavior without a check that fails when that behavior breaks. One meaningful test is more useful than a coverage number; use enough tests for the risk.
5. **Speed:** material regressions are defects. Small hot-path improvements are suggestions unless the product has a strict measured budget.
6. **Simplicity:** dead code or unused options, speculative features, existing helpers that could be reused (name the path), dependencies for trivial behavior, one-implementation abstractions, unused configuration, pass-through wrappers, near-copies that must change together, and functions/classes doing unrelated jobs. Split by responsibility, never by line count.
7. **Human-facing completeness:** requested journeys, comprehensible content, accessible actions, meaningful state feedback and recovery. Source-only review can identify risks, but rendered evidence is needed to verify the interaction.

## Verify each finding

Require a concrete reachable situation and a specific adverse result. Re-read the relevant lines, callers and conditions. Before calling something unused, search the whole relevant tree, including tests, configuration and string/dynamic references. Separate observation from inference.

A `shortcut:` comment documents a decision. Check its ceiling, trigger and whether it still satisfies protected requirements. It is a finding when the limit is exceeded, the assumption is false, or it violates security, accessibility, data integrity or the accepted contract. A marker never excuses those defects.

Propose the smallest complete fix. Deletion and reuse are useful where they preserve behavior. Avoid speculative layers, style preferences, vague worries and ungrounded “consider” findings.

## Report

Start with two or three sentences explaining what the change or repository does, the review scope and expected load. Group numbered findings by:

- **Must fix:** correctness, security, data loss, broken contracted behavior or failure at expected load.
- **Should fix:** risky untested logic, material slowness, damaging duplication, mixed responsibilities or unnecessary code.
- **Nice to have:** optional small speed or clarity improvements.

Each finding includes location, what the code does, the concrete problem, the smallest fix and the consequence of leaving it. Explain unfamiliar terms. Skip empty groups. For a large audit, present at most 20 findings and state any additional lower-priority count only if actually recorded.

Finish with a verdict tied to the reviewed scope and evidence, plus material untested areas. Report potential line/dependency reductions only if counted; those are proposed deletions, not proof of token, time or cost savings. With no findings, say what was checked and that no actionable findings were found within that scope. Do not imply an exhaustive security certification.
