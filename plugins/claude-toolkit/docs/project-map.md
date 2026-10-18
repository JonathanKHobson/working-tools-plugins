# Claude Toolkit project map

- `.codex-plugin/plugin.json`: native source metadata and discovery entrypoint.
- `skills/claude-operation/SKILL.md`: one primary provider operation skill.
- `skills/claude-operation/references/`: CLI, task-fit, computer-use, and model-evidence guidance.
- `scripts/claude_worker.py`: dependency-free bounded text helper; host paths are configurable.
- `README.md`: package boundary and installation-state notes.

Host account state, live receipts, and machine-specific paths belong in the
receiving project's dated capability record, not this portable plugin.
