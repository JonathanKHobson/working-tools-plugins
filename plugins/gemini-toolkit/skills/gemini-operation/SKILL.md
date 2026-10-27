---
name: gemini-operation
description: Operate Gemini through the authenticated Antigravity CLI, with permission-aware headless runs, bounded UI fallback, and task-fit evaluation.
---

# Gemini operation

Use this skill when Gemini or Antigravity is a plausible worker. Start with a
single authenticated bundled `scripts/gemini_worker.py` run for bounded supplied-text work, automatically using its tracked route when configured. Use direct `agy` only for diagnostics or capabilities the wrapper cannot provide.
Pin a model from `agy models`, choose effort deliberately, and capture the JSON
receipt. Headless execution has no interactive approval prompt: unapproved
tools may be soft-denied, so inspect stderr and the completion status.

Keep trivial or inseparable work local when briefing and checking would cost
more than doing it directly. Do not claim token, time, or cost savings without
measurement. A model list is not a dispatched job or a quality result.

- Use the bundled `scripts/gemini_worker.py` for instrumented bounded runs. Direct
  `agy` commands remain valid for diagnostics but are outside the usage tracker.
- Read [CLI operation](references/cli-operation.md) for invocation, sandbox,
  permissions, output formats, and bounded recovery.
- Read [task fit](references/task-fit.md) when routing among Gemini, Claude,
  and local models. Treat strengths as hypotheses and validate the actual task.
- Read [computer use](references/computer-use.md) only when a live browser or
  screen is required.
- Read [model evidence](references/model-evidence.md) for the dated host list;
  refresh it before relying on availability claims.

The skill does not authorize account login, external communication, paid API
use, global permission broadening, or file publication. A model list is not an
inference receipt, and a successful response is not proof that requested tools
ran.
