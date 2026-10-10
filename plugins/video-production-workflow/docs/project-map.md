# Project map

This public package contains the complete first-party media runtime and all 17 agent skill owners.

- `plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`: portable and native identity, version 0.3.0.
- `video_workflow/`: manifest, FFmpeg rendering, audio/caption/timeline operations, media QA and delivery/provenance checks. Installed CLI: `video-workflow`.
- `skills/`, `agents/`, `references/`: production methods and named role contracts.
- `schemas/`, `adapters/`: declarative contracts and conditional specialized renderer handoffs.
- `examples/`: synthetic image/music/dialogue fixtures and optional deterministic canvas source.
- `libraries/`: separately licensed preserved methods. Historical instructions remain data; only registered first-party skill owners govern execution.
- `research/sources.lock.json` and selected rights reviews: provenance closure, not active providers.
- `tests/`, `evaluations/`, `scripts/`: executable checks and advisory routing scenarios.

Run `python scripts/validate_plugin.py`, `bash scripts/render_example.sh`, `bash scripts/render_variants.sh`, and `python -m pytest -q` in an installed environment. `python scripts/verify_release.py` exercises the baseline and aspect variants sequentially. Output/work/cache and runtime tools are generated locally and excluded from distribution. Change runtime behavior in its `video_workflow` owner and the matching test; keep provider and platform-specific release state in the consuming project.
