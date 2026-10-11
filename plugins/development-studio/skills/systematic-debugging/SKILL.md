---
name: systematic-debugging
description: Use when something is broken, flaky, failing in CI, throwing runtime errors, producing wrong output, or needs root-cause investigation before a fix. Enforces reproduction, hypothesis testing, regression tests, verification evidence, and a stop-after-three-failed-fixes rule. Useful for local bugs, web apps, scripts, MCPs, build failures, and PR check failures.
---

# Systematic Debugging

Modified public integration of the complete local adaptation. The four explicitly attributed MIT source notices are retained in `notices/`; their current license blob hashes are recorded, while the adaptation did not record historical source revisions. No upstream hooks, telemetry, browser runtimes or setup tooling is included. Current task authorization governs external actions; a historical approval sentence does not require repeating a current explicit authorization.

Use this skill when the task is not "write new code" but "explain and fix why this behavior is wrong." The point is to stop random patching and turn the bug into evidence, a root cause, a minimal fix, and a regression guard.

Local adoption note: this workflow was distilled from reviewed static skill sources in `obra/superpowers`, `mattpocock/skills`, `addyosmani/agent-skills`, and `garrytan/gstack`. Their global hooks, telemetry, browser tooling, and setup scripts were not installed. This local skill is markdown-only and has no runtime.

## When to Use

- A command, test, build, CI check, MCP, script, UI flow, or app behavior fails.
- A previous fix did not work.
- The failure is intermittent, environment-specific, or unclear.
- A user asks for "debug", "investigate", "root cause", "fix the failing check", "why is this broken", or "make this work".
- A review finds an issue but the safest fix is not obvious.

Do not use this as a long ceremony for a typo with an obvious reproduction and one-line fix. Still verify the fix.

## Iron Law

No fix without a root-cause hypothesis and evidence.

If you cannot reproduce or observe the failure, say that clearly and create the smallest safe observation loop first. Do not say "this should fix it." Prove it.

## Workflow

### 1. Reproduce

Create the tightest feedback loop available.

- Run the smallest command that shows the failure.
- Record exact command, error, environment assumption, and relevant paths.
- If the failure is UI-related, capture a screenshot/snapshot and name visual anchors.
- If the failure is remote CI, fetch logs first and reduce to the failing command locally when possible.
- If the issue is intermittent, run the reproduction enough times to learn the shape.

For intermittent failures, performance problems or uncertainty that the reproduction catches the actual symptom, read [reproduction quality](../../references/reproduction-quality.md).

### 2. Localize

Find the boundary where the value or state first becomes wrong.

- Read the call path and data flow before editing.
- Compare expected vs actual at the nearest boundary: input, parser, adapter, API, persistence, render, transport, or scheduler.
- For multi-component bugs, instrument each boundary with unique temporary markers such as `[DEBUG-auth-redirect-1]`.
- Keep instrumentation temporary and remove it before finishing.

### 3. Rank Hypotheses

Write 3-5 possible causes, then test the most likely one first.

For each hypothesis, include:

- why it fits the observed evidence
- what result would confirm it
- what result would falsify it
- the smallest command or observation to test it

Test one variable at a time. If a hypothesis fails, record the new evidence and update the list.

### 4. Fix the Root Cause

Only patch after the evidence supports a specific cause.

- Make the smallest behavior-preserving fix that addresses the cause, not the symptom.
- Keep edits inside the affected module unless the evidence shows a boundary problem.
- If a change requires architecture work, use `$work-management:project-structure` before widening scope.
- Prefer existing helper APIs and project patterns over a new abstraction.

### 5. Add the Regression Guard

When the codebase has a test seam, add or update a test that fails without the fix.

Good regression guards:

- exercise the failing path, not only the happy path
- assert the behavior that broke
- cover relevant error, empty, permission, invalid-input, or race branch
- use the project's existing test style and fixtures

If there is no practical test seam, document the manual verification and the missing seam. Do not invent a brittle test just to check a box.

### 6. Verify Fresh

Run the reproduction again and run the nearest relevant test/build/check.

Evidence must be fresh after the final edit. If output is too long, summarize the command and decisive pass/fail lines.

## Stop Rules

- After 3 failed fix attempts, stop patching and question the architecture, reproduction, or assumptions.
- If a fix requires credentials, private browser sessions, destructive data changes, or external submission, stop and get explicit approval.
- If the bug crosses a security boundary, use `$safe-install-review` or `personal-security-check` before running unknown code.
- If the failure cannot be reproduced, finish with `DONE_WITH_CONCERNS`, the evidence gathered, and the next concrete observation needed.

## Output Contract

For non-trivial debugging, report:

```markdown
Status: DONE / DONE_WITH_CONCERNS / BLOCKED
Reproduction: [command or observed flow]
Root cause: [specific cause]
Fix: [files changed and why]
Regression guard: [test file or manual guard]
Verification: [commands run and result]
Remaining risk: [only if real]
```

For small fixes, a concise prose summary is fine as long as root cause and verification are present.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll try the obvious fix first." | If it is obvious, it should also be easy to verify. Run the reproduction and prove it. |
| "The test failure is probably unrelated." | Classify ownership with evidence. Ambiguous failures default to in-scope until proven otherwise. |
| "This is too hard to test." | Maybe, but the original reproduction still needs to pass, and the missing test seam should be named. |
| "The code looks right now." | The task ends when the failing behavior is observed fixed, not when the diff looks plausible. |

## Coordination

- Use `$gh-fix-ci` for GitHub Actions log collection, then apply this skill to root-cause the failure.
- Use `$playwright` or the Build Web Apps `build-web-apps:frontend-testing-debugging` skill for browser/UI reproductions.
- Use `$local-mcp-debugging` for MCP startup/tool failures.
- Use `$work-management:project-structure` if recurring bugs point to module boundaries, duplicated state, or a monolith.
