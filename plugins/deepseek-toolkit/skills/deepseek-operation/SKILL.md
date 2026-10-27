---
name: deepseek-operation
description: "Use DeepSeek for a bounded alternative solution, code or source critique, checkable reasoning, or a bilingual interpretation trial; verify access, output and returned model."
---

# DeepSeek operation

Use this toolkit when another model family can contribute a checkable alternative while the lead continues independent work. Keep trivial and inseparable tasks local. Work Management owns common routing; the domain owner owns the actual deliverable and validation.

## Choose the route

The bundled `scripts/deepseek_worker.py` at the plugin root runs supplied-text tasks through NVIDIA's hosted DeepSeek endpoint. It has no browsing, file, shell, MCP or agent tools. Supply the required evidence and check its response. An API response is not a source or an independent corroboration of another model.

The configured endpoint is `https://integrate.api.nvidia.com/v1/chat/completions`, requesting `deepseek-ai/deepseek-v4.1-flash`. The service advertises a free developer endpoint as of October 22, 2026. Free access is subject to provider availability, quotas and trial terms. Never switch to a paid endpoint or purchase credits automatically. Do not claim a permanent free entitlement. This is NVIDIA-hosted DeepSeek, not a DeepSeek consumer-chat subscription or local model.

Read [CLI operation](references/cli-operation.md) for setup, commands and recovery, and [model fit](references/model-fit.md) when selecting a task or discussing cultural perspective. Consult the host capability record for the current verified state. Source files and a configured key do not prove a working inference.

## Execute and verify

1. Resolve the installed helper from this package and run `python3 /resolved/plugin/scripts/deepseek_worker.py --check`. This checks local configuration only; `inferenceTested: false` is intentional. Never print or read a key into chat.
2. Give one compact brief: output, supplied sources, protected requirements, acceptance check and stop condition. Use only material authorized for NVIDIA processing. Its trial notice records inputs and outputs for the trial and improvement; do not send confidential project files or personal information merely because the CLI can access them.
3. Send the brief on stdin with `--json`, an appropriate output cap and a bounded timeout. Retain the running handle; do not duplicate a slow job. The helper does not retry or fail over.
4. Inspect nonempty result, terminal status, truncation/finish reason, actual returned model and reported token usage. Requested identity is not proof of the served snapshot, and model self-description proves nothing. An unreported model remains unknown. NVIDIA's alias must not be labeled DeepSeek's newer direct-API snapshot without evidence.
5. Verify material claims against the original sources and code or calculation results. Integrate a useful contribution or reject it with a concrete reason. Different wording, disagreement and agreement do not establish added value.

The optional existing host recorder receives metadata only after each actual text inference attempt. Checks, setup and invalid input do not count. Recording failure must never block the task. See the CLI reference for coverage limits; interactive terminal-agent use is separate from this helper.

For missing credentials, expired access, throttling or an unavailable model, report the actual error category. Keep the task local or ask for the missing account action. Do not infer signed-out status from a generic network failure, rotate accounts to evade limits, scrape consumer sessions or enable paid fallbacks.
