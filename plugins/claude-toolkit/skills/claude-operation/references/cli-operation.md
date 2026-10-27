# Claude delegation

Use when Claude is a suitable worker. The entrypoint owns the common scope and acceptance checks. Work Management may coordinate a larger job; this toolkit works without that optional companion. Retain the receiving user's tone and delivery preferences.

## Start with the subscription CLI

Use the official subscription-authenticated CLI first when the receiving user has authorized Claude delegation, including standing authorization. Do not wait for a per-task request to select Claude. Desktop or Web is appropriate when the user explicitly requests it, the task needs a
feature available only through that interface, or the CLI still fails after
bounded diagnosis and official login recovery. Missing authentication alone is
not a reason to switch surfaces. Preserve existing jobs across all surfaces.

Desktop login and terminal login are separate. Recheck CLI authentication before each dispatch. The toolkit bundles `scripts/claude_worker.py` at its package root. Set `CLAUDE_WORKER_HELPER` to that discovered file path; choose a supported Python 3 runtime and locate the recipient’s official Claude CLI through PATH or the helper’s `--cli` option. No author-machine path is required.
Keep individual recovery receipts and unresolved causes in the owning project.

For supplied-context critique, drafting or extraction, check authentication:

```sh
python3 "$CLAUDE_WORKER_HELPER" --check
```

Pass a compact authorized task on stdin to the same command without `--check`.
Select the model suited to the task after verifying live availability and the user's preferences. Use the supported CLI
alias, such as `--model opus`, and `--json` to record the returned actual model
from the inference receipt; an alias or selected name alone does not prove the
version used. If the preferred version is unavailable, report the verified
model actually used and choose a suitable available model within task scope.
Inspect the recipient helper's actual default and pass a model explicitly when a particular one was selected. Pass `--effort medium` or `--effort high` when supported and warranted; do not leave a hard problem on a helper's low default by accident. Distinguish requested effort from returned model identity: a requested-effort receipt does not prove server-side effort. Report only model identity supported by returned metadata.

The helper has no file-editing, shell, browsing, MCP or skill tools; the lead
supplies the evidence and validates the result. It stops on failure or timeout
without retry, stores no session, and does not start a daemon. Do not mistake
authentication-only `--check` for an inference test. The helper is bundled; the recipient’s Claude executable, login and task records remain external. Installing method files does not authenticate the backend.

Use the bundled `scripts/claude_worker.py` for tracked bounded work. It records one
fail-open usage event around each real inference attempt. Direct `claude` calls and
authentication checks are intentionally outside that tracker.

The helper strips inherited API/provider overrides, ignores custom settings,
checks first-party subscription auth, and uses `--safe-mode --restricted`, an
empty tool set and strict empty MCP config. **Do not use `--bare` for this
subscription route**: the installed version disables OAuth/keychain lookup in
bare mode. Do not extract tokens or build a generic OAuth proxy.

## Bounded diagnosis and login recovery

On missing auth, start the official `claude auth login --claudeai` in an
interactive terminal and follow the URL supplied by that running login process.
Prefer the visible Codex in-app browser for reviewable authentication; reuse an
existing authenticated browser session when it can complete the official flow.
Finish supported routine sign-in and consent steps within the user's authorized
scope. Keep the login terminal alive for its callback, then check its exit and
run `claude auth status` before retrying the worker once. Record a sanitized
receipt, never credential values, tokens, or the full transient OAuth URL.

Ask the user to act only when an actual provider or tool requirement needs them,
such as an MFA approval unavailable to the agent, a CAPTCHA confirmation, required
personal confirmation, a new password, or terms acceptance. State the specific
requirement and preserve the pending flow where
possible. Do not assume every sign-in requires the user, and do not promise that
future logins will always be unattended.

A failed authentication command is not proof of a signed-out account. Distinguish explicit `loggedIn: false` from command, sandbox, keychain, network or malformed-output failures. Diagnose in the same execution environment and use its authorized access mechanism; do not bypass its restrictions or describe a native fallback as proof Claude is unavailable.

For other CLI failures, inspect the concrete error, installed CLI/help,
auth/provider state and helper/runtime availability. Apply one justified fix
and retry once; stop repeated recovery attempts when the same failure remains.
Use Desktop or Web only if that bounded recovery leaves a real CLI blocker and
the alternate surface can complete the authorized task. Report the blocker and
chosen surface. A subscription quota limit is a shared capacity constraint, not
a reason to duplicate jobs across surfaces or providers.

Never use `--console`, an API-key fallback, extra usage credits or a provider
switch to evade subscription limits. Estimated list-price fields in CLI output
are not billing receipts. Claude Chat, Design and Code share plan capacity.

Code-editing delegation is a different scope: verify checkout ownership and
authorize only the needed tools in an isolated workspace. This text helper does
not establish unattended coding safety. On another host, discover and validate
the local CLI/runtime rather than copying host paths or credential stores.

## Conditional Desktop or Web route

Verify the live account and model picker when this surface is warranted; dated
Desktop receipts do not establish current availability. Apply the task-based model selection in [Claude delegation](../SKILL.md), verify the selected model and record it.

Create a separate Chat or Code task. Existing Code work may continue in the
background; do not stop it just to start a chat. One controller owns the app UI.
Prefer a separate empty composer. If temporarily reusing a shared New Chat
composer, preserve any existing draft exactly, check for concurrent edits, then
restore it after submission. Never submit the unrelated draft.

For analysis-only Chat requests, supply all needed evidence and ask for no tools,
files, browsing, or execution. This is requested scope, not a technical sandbox.
Code work needs checkout/file ownership and relevant project instructions. Do
not change global permission modes for convenience. Read the completed response,
separate advice from evidence, and integrate useful findings. Sent or streaming
is unfinished.

Other routes and live setup owners are recorded at
the receiving host’s existing private capability record.
Read it only when choosing workers; dated entries are not proof of live availability.
Prepaid access still has quota and energy costs. Recheck availability on failure;
do not continuously poll or duplicate jobs across providers.

Official references:
[subscription login](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan),
[CLI reference](https://code.claude.com/docs/en/cli-usage),
[usage limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work).
