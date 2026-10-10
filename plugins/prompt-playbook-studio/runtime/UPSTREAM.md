# Pinned compiler provenance

- Upstream: [SpannDaMan/prompt-optimizer](https://github.com/SpannDaMan/prompt-optimizer)
- Reviewed commit: `cef400f53473571cfec56f8f67d4deda9fd6e38b` (main on 2026-09-29)
- Copied file: `plugins/prompt-optimizer/scripts/prompt_optimizer.py`
- Copied file SHA-256: `283a3c0e9978cd961ea738b6d8a523cd13c014ed2b3b48bacdf777eadefad4d7`
- Upstream code and package version at that commit: `0.1.7`; a separate marketplace listing reported `0.1.9`. The commit and file hash, not that listing, identify this copy.
- License: MIT; original notice is retained in [LICENSE](LICENSE).

The vendored Python file is unchanged. The adjacent wrapper only loads its fixed local path. We did not copy the upstream skill's automatic four-sentence activation rule, plugin manifest, hooks, release tooling, example prompts, or tests into the runtime package.

The reviewed runtime imports only Python standard-library modules (`argparse`, `hashlib`, `json`, `re`, `sys`, `dataclasses`, `pathlib`, and `typing`). Its commands read caller-selected local files, optionally create one new scaffold file, and write analysis, validation, trace, ledger, or render output to stdout. There is no network, provider, telemetry, package install, plugin loading, or prompt/task execution path in the copied runtime. A packet stores the exact original prompt and should be treated as sensitive local data.
