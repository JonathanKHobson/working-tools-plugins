# Claude Toolkit

Claude Toolkit is the provider owner for Claude operating guidance. It is
CLI-first: use the subscription-authenticated Claude Code CLI when the task is
independent and the user has authorized delegation, then verify the receipt and
the useful output. The toolkit does not grant credentials, paid API access, or
permission to send external messages.

The primary skill is `claude-operation`. It routes CLI, bounded computer/UI
fallbacks, and task-fit evaluation. Read the linked references only for the
mode being used. Host-specific paths and live capability claims belong in the
receiving host's dated capability record.

This source plugin is a candidate for native installation. Installed, signed,
or marketplace status must be verified separately; source presence is not
installation or publication proof.


## Set up your own environment

1. Obtain the official [Claude Code CLI](https://code.claude.com/docs/en/setup) for your supported operating system. Use your own account and plan; this plugin supplies no credentials or entitlement.
2. Locate `claude` on PATH and run `claude auth status`. For missing subscription login, use the official `claude auth login --claudeai` flow; enter passwords and MFA only in the provider flow.
3. Locate this installed package’s `scripts/claude_worker.py`. It requires Python 3 on a POSIX host and the Claude CLI; it has no Python package dependencies. Set `CLAUDE_WORKER_HELPER` to that file. For a CLI outside PATH, pass `--cli /your/claude` or set `CLAUDE_CLI`.
4. Run `python3 "$CLAUDE_WORKER_HELPER" --check`. This verifies authentication only. Then send a small nonprivate task from a file on stdin with an explicit model/effort and `--json`; verify actual modelUsage and answer before routine delegation.
5. Keep your own task prompts and receipts in your project, outside the plugin. If no CLI, supported Python, login or allowance exists, report that dependency; do not enable API billing as a substitute.

The bundled text helper disables tools, MCP and custom settings. It is suitable for supplied-context work; it cannot browse or implement file edits. Full coding uses the official CLI in an owned checkout with separately scoped tools. Read [CLI operation](skills/claude-operation/references/cli-operation.md) before dispatch. No account details or live service bindings are distributed.
