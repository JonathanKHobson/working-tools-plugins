<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Optional Codex host hooks

This repository-level integration provides the author's two previously local hook behaviors as a reviewed, portable edition. `UserPromptSubmit` detects likely artifact review obligations. `Stop` reports pending obligations for the same scope, or provides a reminder to close resources actually started by that chat. It does not perform reviews or clean up resources. Nothing here registers, installs or trusts hooks automatically.

This extends [Work Management Studio](https://github.com/JonathanKHobson/working-tools-plugins/tree/main/plugins/work-management/) closeout guidance and the review routes in [Writing Quality Studio](https://github.com/JonathanKHobson/working-tools-plugins/tree/main/plugins/writing-quality-studio/), [UX Design Studio](https://github.com/JonathanKHobson/working-tools-plugins/tree/main/plugins/ux-design-toolkit/), [Graphic Design Studio](https://github.com/JonathanKHobson/working-tools-plugins/tree/main/plugins/graphic-design-studio/) and [Figma Design Toolkit](https://github.com/JonathanKHobson/working-tools-plugins/tree/main/plugins/figma-design-workflow/). Those workflows are optional review aids. The Python runtime has no plugin dependency. This folder is an optional integration, outside the package registry and marketplace catalogs.

## Behavior and limits

`quality_rules.py` preserves the local source's classifier and review routing: visual artifacts suggest `visual_qa` and `design_taste`; audience-facing copy suggests `communication_review`; technical configuration context suppresses many incidental matches. These are keyword heuristics. For example, “What does this email mean?” still suggests a communication review. Use `quality skip` with a reason when the detected check does not apply.

Each valid submitted prompt with a scoped ID replaces that scope's earlier obligations, including clearing them for a nonvisual prompt. Missing/empty prompts leave state unchanged. This models the newest request, not a durable project checklist; follow-up questions can replace earlier checks. Pending checks cause one Stop continuation (`decision: block`). A reentrant Stop with `stop_hook_active: true` is silent, preventing a continuation loop. No ID means no state access and no blocking decision.

Session IDs take precedence over turn IDs to support continuations. Turn IDs are a fallback only. Separate sessions have separate files. No workspace fallback or global “active session” is used. Overlapping turns sharing a session update the same record; use separate sessions for independent work.

Only SHA-256 scope keys, schema version, timestamp, obligation names/statuses and attestation/reason-presence flags are stored. Raw IDs, prompts, prompt hashes, transcripts, workspace paths and reviewer/evidence/reason prose are never stored. The hook reads the bounded JSON payload from stdin but ignores transcript paths and other private fields. CLI review text is transient and can still appear in the caller's shell history or Codex tool logs, so use minimal nonsensitive descriptions.

This is a portable adaptation of the two registered lifecycle behaviors. It requires an explicit session or turn ID instead of using the original environment or workspace fallback, and replaces the original persistence and manual review state. It does not reproduce the author's entire private diagnostic CLI. Global process/MCP/config scans, private path bindings, prompt previews, memory/KSB logging, pressure-helper integration and unrelated diagnostic modes are deliberately excluded. There are no network calls, subprocess launches, process-kill commands or memory writes in the runtime. See [provenance.json](provenance.json) for the source hashes and transformation scope.

## Download

Get `codex-host-hooks-0.1.0.zip` and `SHA256SUMS.txt` from the [v0.1.0 release](https://github.com/JonathanKHobson/working-tools-plugins/releases/tag/codex-host-hooks/v0.1.0). Verify the archive checksum, extract it and follow the manual setup below. The archive contains this integration, tests and licenses. It contains no personal configuration or state.

## Requirements and files

Use Python 3.9+ on macOS or Linux with `fcntl`, directory file descriptors, `O_NOFOLLOW` and POSIX modes. Native Windows is unsupported. A local filesystem with reliable locks is required; network shares are unsupported for state. Use an absolute interpreter path in the hook definition and an absolute reviewed script path. Keep these three runtime files together:

- `codex_host_hooks.py`: hook stdin/stdout and manual quality CLI.
- `quality_rules.py`: operative classifier and review routing.
- `scope_state.py`: bounded, private state and locking.

Configure a dedicated absolute state directory with an existing parent. The runtime can create the final directory as `0700`; if it already exists, it must be owned by the current user and exactly `0700`. Record and lock files must be owned regular files with mode `0600` and one hard link. Every state path component is opened without following symlinks. On macOS, canonical paths such as `/private/tmp/...` may be necessary because `/tmp` is a symlink. Do not configure a shared directory or check state into Git.

Malformed or oversized hook input, unusable state, failed locks and invalid schemas fail open: exit zero, no blocking output, a generic stderr diagnostic. Hook input and state reads are limited to 64,000 bytes. Failed quality commands exit 2. A missing record is clear; corrupted records cannot be marked complete. This fail-open policy protects task continuity and is not an enforcement guarantee. A terminated write may leave an invalid record that requires clearing or deleting the specifically identified file after review. Files accumulate until manually removed; there is no background service or automatic retention cleanup.

## Review and manually register

1. Read all three runtime files, this README, provenance and the tests. Run the isolated test command below. Choose an interpreter, script location and private state directory on your own host.
2. Inspect your existing Codex hook sources. Back up the exact configuration you intend to edit. `hooks.example.json` is a template with deliberately invalid placeholders; do not copy it unchanged. Replace `REVIEWED_PYTHON_ABSOLUTE_PATH`, `REVIEWED_SCRIPT_ABSOLUTE_PATH` and `PRIVATE_STATE_DIRECTORY_ABSOLUTE_PATH`. Preserve shell quoting and ensure the resulting commands match the files you reviewed. Use only trusted paths; hook commands run through a shell.
3. Add the two event entries to your chosen source manually. Preserve existing event arrays and unrelated entries rather than overwriting them. Prefer one representation in a layer. Use project-local `<repo>/.codex/hooks.json` for project scope, or `~/.codex/hooks.json` for user scope. This optional integration supplies neither a plugin manifest nor an activation command.
4. Open `/hooks` in Codex CLI, inspect the exact definitions and explicitly review/trust them. Repeat review when a definition changes. Project-local hooks also require a trusted project configuration layer. Verify both events using synthetic prompts and disposable state before using real work.

Codex accumulates matching hooks from active sources. Installing or enabling a plugin does not trust its hooks. Review exact definitions, duplicates and prior sources before adding this pair. See the [official Codex hooks documentation](https://learn.chatgpt.com/docs/hooks) for current discovery, trust and event schemas. This integration has passed isolated tests; live native registration/trust is the recipient's separate step.

## Record a review or skip

Use the exact same configured interpreter, script and state directory. Replace the placeholders in these examples. Identify the scope using `--session-id`, `--turn-id`, or the opaque `--scope-key` from a previous status response. If neither ID flag is passed, `CODEX_SESSION_ID` then `CODEX_TURN_ID` is used when your host actually supplies it. Do not assume those environment variables exist or select another session merely to clear a block.

```sh
REVIEWED_PYTHON_ABSOLUTE_PATH REVIEWED_SCRIPT_ABSOLUTE_PATH --state-dir PRIVATE_STATE_DIRECTORY_ABSOLUTE_PATH quality --session-id CURRENT_SESSION_ID status
REVIEWED_PYTHON_ABSOLUTE_PATH REVIEWED_SCRIPT_ABSOLUTE_PATH --state-dir PRIVATE_STATE_DIRECTORY_ABSOLUTE_PATH quality --session-id CURRENT_SESSION_ID mark visual_qa --reviewer 'manual render review' --evidence 'checked accepted anchors and relevant states'
REVIEWED_PYTHON_ABSOLUTE_PATH REVIEWED_SCRIPT_ABSOLUTE_PATH --state-dir PRIVATE_STATE_DIRECTORY_ABSOLUTE_PATH quality --session-id CURRENT_SESSION_ID skip design_taste --reason 'No visual artifact was produced'
```

Quote each substituted filesystem path according to your shell, especially paths containing spaces. `mark` requires nonempty reviewer and evidence; `skip` requires a nonempty reason. Each value is capped at 4,096 UTF-8 bytes. Only already detected checks can be updated. Marking records the caller's attestation and does not execute a reviewer or verify the evidence. State/status output explicitly reports `independent_verification: false`. Keep actual review evidence in the owning project, subject to its privacy rules.

## Testing

From this folder:

```sh
python3 -B -m unittest discover -s tests -v
```

The tests create isolated temporary directories and synthetic IDs. They never read or modify your real Codex configuration or hook state. Coverage includes operative classifier cases and ambiguity, nonvisual requests, prompt parsing, malformed/oversized input, missing scopes, two-session isolation, turn fallback, replacement semantics, reentrant Stop, completion/skip, empty attestations, prompt privacy, modes, symlink/hardlink rejection, corrupt records and scoped clearing. A real hook payload and native trust flow remain host-specific acceptance steps.

## Disable and rollback

Use `/hooks` to disable these exact non-managed definitions. Remove only the two entries you added, or restore your configuration backup if it contains no later changes. Inspect all active sources to confirm that another copy is not still configured. Leave unrelated hooks intact. No plugin uninstall or process cleanup is needed for this integration.

`quality ... clear` removes only the current scope's validated state record and reports clear. Its empty lock file remains. After disabling all users of a dedicated state directory, you may remove that directory manually using your normal file tools. Never recursively remove a directory you did not exclusively create for this integration. Removing source or clearing state does not revoke native hook trust; use the host's `/hooks` controls.

## License and attribution

Original author: Jonathan Kyle Hobson (Kyle Hobson). First-party Python source and tests are AGPL-3.0-only. This README, example configuration and provenance are CC BY-SA 4.0. Parent repository [licensing](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/LICENSING.md), [code license](LICENSE-CODE-AGPL-3.0.txt), [documentation license](LICENSE-DOCS-CC-BY-SA-4.0.md), and [notice](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/NOTICE.md) apply. Earlier upstream grants remain unchanged; this integration adds no third-party implementation dependencies.
