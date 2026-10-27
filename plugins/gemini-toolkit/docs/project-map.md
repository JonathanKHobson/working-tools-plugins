# Gemini Toolkit project map

- `.codex-plugin/plugin.json`: native source metadata and discovery entrypoint.
- `skills/gemini-operation/SKILL.md`: one primary provider operation skill.
- `skills/gemini-operation/references/`: CLI, task-fit, computer-use, and model-evidence guidance.
- `README.md`: package boundary and installation-state notes.
- `scripts/sync_antigravity.py`: deterministic Antigravity plugin and skill-link reconciliation. It requires an explicit host-private JSON config for paths and collision owners; `--check` is read-only, while `--apply` snapshots managed paths and rolls back on a failed native operation. `tests/test_sync_antigravity.py` uses a fake native CLI and never starts a model or hook.

Host account state, live receipts, and machine-specific paths belong in the
receiving project's dated capability record, not this portable plugin.
