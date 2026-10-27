# CLI operation

## Text worker

The helper uses Python's standard library. No package installation or background service is required. Resolve its path from the installed toolkit.

```sh
python3 /resolved/plugin/scripts/deepseek_worker.py --check
python3 /resolved/plugin/scripts/deepseek_worker.py --set-key
python3 /resolved/plugin/scripts/deepseek_worker.py --json --max-tokens 4096 --timeout 300 < brief.txt
```

`--set-key` prompts without echo and stores the key in the user's private `~/.config/deepseek-toolkit/nvidia-api-key` file with mode 0600. An explicitly supplied `NVIDIA_API_KEY` takes precedence; `DEEPSEEK_API_KEY_FILE` can select a different private file. Never put keys in command arguments, source files, examples, receipts or shell history.

The check reports local credential configuration, not API authentication or quota. A real response is needed for inference verification. Inspect the returned `model`, result and finish reason; preserve unknown fields. A quota or access error is not permission to buy credits. There are no automatic retries or alternative providers.

The worker submits a single text task. It does not read the current directory, search the web, call tools or edit files. Give it source excerpts explicitly and perform any required verification with the lead's tools.

## Optional interactive coding client

A recipient may separately install and configure a coding client such as [OpenCode](https://opencode.ai/docs/providers/#nvidia). This package does not install a `deepseek` command or configure that client. Filesystem access, tools, provider selection, auxiliary requests, updates, sharing, state storage and approvals belong to the recipient's explicit client configuration. Check the [OpenCode configuration reference](https://opencode.ai/docs/config/) and native client state before claiming any of those controls are active.

Keep coding-client sessions separate from the bundled text worker. They may access files and tools when authorized, and their usage is outside this helper's tracking coverage. Do not infer that a private host launcher or its configuration exists on another machine.

## Usage coverage

Each actual bounded text-worker attempt emits one optional `provider=deepseek`, `plugin=deepseek-toolkit` completion event through the host's existing `~/.config/studio-tools/usage-tracking.json` recorder binding. It records status, duration, requested and explicitly returned identity and provider-reported input/output tokens. Missing token values remain unknown. It stores no prompts, responses, keys or paths.

This is instrumented helper usage, not complete account usage, billing, remaining quota or measured time savings. Direct API calls, web chat and interactive OpenCode sessions are outside this helper's tracking coverage. Do not repeat an inference merely to add a tracker event. Tracking starts no models, polling, recurring jobs or services.

Public provider documentation checked October 27, 2026: [NVIDIA endpoint](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash), [OpenCode NVIDIA provider](https://opencode.ai/docs/providers/#nvidia), [OpenCode configuration](https://opencode.ai/docs/config/).

## Slow endpoint responses

The helper's maximum and default socket timeout is 300 seconds. That is a wait limit, not a response-time or availability guarantee. Keep the existing job handle while it is active. After a timeout or provider error, report the observed category and continue with another authorized path; do not queue duplicate inference attempts or enable paid fallback automatically. No live endpoint or account check was performed for this public package preparation.
