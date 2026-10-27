# DeepSeek Toolkit

- `plugin.json`: portable plugin identity and presentation.
- `.codex-plugin/plugin.json`: native Codex compatibility metadata.
- `skills/deepseek-operation/SKILL.md`: route selection and verification.
- `skills/deepseek-operation/references/`: setup, recovery, task fit and source limits.
- `scripts/deepseek_worker.py`: one bounded NVIDIA text inference and optional host usage event.
- `tests/test_deepseek_worker.py`: mocked HTTP, credential and tracking checks.

The terminal coding client and credentials belong to the receiving host. Work Management owns common routing and usage collection. No background server or MCP is required by this toolkit.
