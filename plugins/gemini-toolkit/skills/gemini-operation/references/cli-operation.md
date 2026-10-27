# Gemini and Antigravity CLI operation

Authenticate once through the official interactive Antigravity flow, then use
the cached account for bounded headless runs. Confirm the current account and
model list before relying on a dated capability record.

For bounded supplied-text tasks, resolve the bundled helper from the installed toolkit and use it by default, including its optional host-configured usage recording:

```sh
python3 "$GEMINI_WORKER_HELPER" --model gemini-3.8-flash-medium < "$TASK_FILE"
```

Model availability diagnostics use `agy models`. Direct CLI commands are appropriate only for diagnostics or capabilities the wrapper lacks and remain outside wrapper tracking. The helper keeps sensitive task text off command arguments and accepts it on stdin.

`--output-format json` returns a completion object; `stream-json` is useful for
monitoring tool events and token usage. Pinning an unknown model must fail
loudly rather than silently falling back. Keep the active project directory
empty or explicitly scoped for supplied-context text work.

Antigravity headless mode has no interactive approval prompt. Workspace file
access is generally allowed; commands, web, and MCP operations default to Ask
and may be soft-denied. Prefer `--sandbox` and narrowly scoped allow rules in
`~/.gemini/antigravity-cli/settings.json` when tools are needed. Never use
`--dangerously-skip-permissions` for routine delegation. A plan-mode run is a
useful architecture or review route when file edits are not intended.

Inspect both stdout and stderr, require a successful terminal status, and
confirm the actual model in the receipt when the CLI reports it. Do not infer
model quality from the available-model list. Do not add a paid API key or
switch surfaces to evade subscription limits.

Official references:

- [Antigravity headless mode](https://www.antigravity.google/docs/cli/headless/)
- [Antigravity permissions](https://www.antigravity.google/docs/permissions?tab=cli)
- [Antigravity terminal sandbox](https://www.antigravity.google/docs/sandbox/?tab=cli)
- [Gemini API models](https://ai.google.dev/gemini-api/docs/models)


For supplied text requiring a no-tools guarantee, choose a technically restricted worker instead: Antigravity is tool-capable, and a prompt to avoid tools is not isolation. `--sandbox` restricts terminal execution, not every tool. Version 1.4.2 warns that `--disable-slash-commands` makes `--mode plan` ineffective; do not claim that combination protects files. Inspect stream tool events and effective permissions, recognizing that post-run checks detect rather than prevent side effects.

Keep sensitive prompts off command arguments using the documented stdin protocol: send one JSON line `{"event":"user","message":{"content":"YOUR AUTHORIZED TASK"}}` to `agy --input-format stream-json --output-format stream-json --model SELECTED_ID --print-timeout 5m --sandbox`, then close stdin. Verify current CLI help before adapting; do not also pass `-p` in streaming-input mode. The init model is CLI configuration evidence; backend identity can remain unreported. Require SUCCESS, a nonempty final response and relevant source checks. Retain the running job handle and collect its completed output before claiming success.

For tracked bounded work, invoke the toolkit's `scripts/gemini_worker.py`, which owns
that stdin protocol and records one fail-open usage event for the model attempt. A
direct `agy` invocation is intentionally untracked.
Pass `--receipt-file /absolute/local/path.json` when a review needs CLI init-model,
completion-model, terminal status, token fields, and event counts as separate evidence.
The init-model is the CLI's configured request, not backend model attestation.
