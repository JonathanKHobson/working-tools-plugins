# Claude model evidence

Model evidence is host-specific and dated. Keep the live account, executable
path, alias list, and returned model receipt in the receiving project's
capability record rather than this portable plugin.

Refresh with the installed CLI and record the actual receipt before relying on
any dated record:

```sh
claude --help
claude auth status
python3 "$CLAUDE_WORKER_HELPER" --model opus --effort high --json < brief.txt
```

Availability, selected alias, and returned model identity are separate facts.


Public documentation snapshot, reviewed 2026-10-17: Anthropic documents [Opus 5.5](https://www.anthropic.com/claude-opus-5-5) and [Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5). These pages describe provider-reported capabilities, not every account’s entitlement. Alias resolution can lag a named release; if a particular supported version matters, request its exact ID and inspect returned metadata. Do not rerun an already useful job merely to update its version label. Recheck documentation on a requested model change, access failure or capability review; there is no automatic polling job.
