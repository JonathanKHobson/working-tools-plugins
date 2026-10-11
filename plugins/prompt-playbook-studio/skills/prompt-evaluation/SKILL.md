---
name: prompt-evaluation
description: Compare prompt versions or build repeatable tests for prompt behavior, using observable criteria and preserved run evidence. Use when results or regressions need checking; a simple prompt draft does not require an evaluation suite.
---

# Prompt Evaluation

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Translate the requested outcome into observable checks before testing. Separate factual correctness, instruction following, output structure, usefulness and relevant safety boundaries. Identify the failure a revision is supposed to fix; avoid scoring generic qualities that don't affect this task.

Use a compact set of representative ordinary, ambiguous, missing-input, boundary and adversarial cases. Include a benign near miss for any security check. Each case needs input, expected behavior and a failure condition. Use synthetic records where real personal data is unnecessary. For a tool boundary, assert which action or arguments were allowed or denied, not merely whether the model wrote a refusal sentence.

Compare baseline and candidate on the same cases, model/version, settings and available tools where possible. Repeat only when stochastic variation could change the decision. Preserve outputs and run configuration in the private project. Check objective properties with parsers, schemas, fixtures or receipts; use human judgment for subjective quality and consequential decisions. Model judges can help inspect evidence but are fallible and should not certify their own output.

Report observations separately from proposed tests or predictions. A static review is not a behavioral run. A small passing set is not proof of universal reliability or a percentage improvement. Describe regressions, material tradeoffs and untested conditions. After a meaningful prompt, model, tool, retrieval or policy change, rerun the affected cases rather than automatically rebuilding a large benchmark.

For a security-focused injection or tool-boundary evaluation, use `master-security-toolkit:instruction-security-review` and its finding-to-control tests when that separate plugin is available. If absent, evaluate the source and action boundaries with the first-party cases above and state that a formal audit was unavailable. For prompt creation/refinement, return to `prompt-playbook-studio:prompt-playbook`. Neither an evaluation nor its generated prompt authorizes execution against production services.

## Full procedure requirement

Read this complete evaluation method before testing. Select a relevant original pattern/template through the [native procedure map](../../docs/full-procedures.md) only when it informs the current fixture or expected output; no separate evaluation-method plugin is required. Perform and retain actual runs before reporting a behavioral result.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Prompt Evaluator, Prompt Engineer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
