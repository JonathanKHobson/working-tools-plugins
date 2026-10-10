# Prompt Playbook submission advisory

`scripts/prompt_submit_advisory.py` reads one bounded `UserPromptSubmit` JSON event. It emits a single `hookSpecificOutput.additionalContext` hint only for explicit prompt-crafting requests that lack a target or proportionate success check. It is quiet for ordinary work, prompt-tool implementation, malformed input, and prompts that already have a success check. It does not call Prompt Compass or Knowledge Atlas, save prompt content, change the user prompt, or require another approval.

Codex auto-discovers `hooks/hooks.json` from the installed Prompt Playbook Studio plugin. A recipient must review and trust a non-managed hook definition through `/hooks` before it becomes active; disabling the plugin or revoking that trust stops the advisory. The Claude plugin manifest declares `hooks/claude-hooks.json` with an absolute `${CLAUDE_PLUGIN_ROOT}` command; Claude activation must be reviewed in that host. Disabling the plugin stops its advisory. Keep only one registration per host: remove the former global canonical-script entry when enabling the plugin-owned hook. A source declaration or successful install is not execution proof; use an interactive prompt-crafting turn to verify `UserPromptSubmit`.

The packaged Codex declaration uses a relative script command. It works when the host executes plugin hooks from the installed plugin root; verify that host resolution and trust in a fresh session before claiming the advisory is active. If the host does not provide that working directory, bind the script at the recipient's own stable path in host configuration without changing this distributed package. The Claude declaration uses `${CLAUDE_PLUGIN_ROOT}`. Native hook execution remains a separate acceptance check from package validation.

The legacy `~/.codex/scripts/codex_prompt_submit_gate.py` mixed prompt readiness, pressure scanning, and artifact obligation state. Artifact obligation detection now has a separate `UserPromptSubmit` entry owned by `~/.codex/scripts/codex_artifact_prompt_hook.py`, so removing the old prompt gate does not remove the existing closeout quality check.

Verify locally with a JSON event, for example:

```sh
printf '%s\n' '{"prompt":"Rewrite this prompt."}' | python3 scripts/prompt_submit_advisory.py
```

The expected output is one JSON object with `hookEventName: UserPromptSubmit` and a short advisory. An ordinary request should produce no output and exit 0.
